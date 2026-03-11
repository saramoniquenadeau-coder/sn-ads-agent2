import json
import os
import requests
import anthropic


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_organic_content(brief: dict) -> dict:
    """Generate organic social media content using Claude."""
    platform = (brief.get("platform") or "Facebook").strip()
    tone = brief.get("tone") or "Clinique, calme, humain, rassurant"
    audience = brief.get("audience") or "Familles"
    objective = brief.get("objective") or "Contenu éducatif organique"
    topic = brief.get("topic") or "Soins infirmiers à domicile"
    content_format = brief.get("format") or "educational"

    system_prompt = (
        "Tu es une infirmière expérimentée qui parle aux familles avec douceur et professionnalisme. "
        "Tu écris du contenu organique (non-publicitaire) pour les réseaux sociaux de SN Soins Infirmiers. "
        "Règles absolues : pas de vente agressive, pas d'urgence artificielle, "
        "pas d'affirmations médicales absolues. "
        "Voix : une infirmière qui parle à une famille, pas une publicité."
    )

    word_limit = "150 mots max" if platform.lower() == "instagram" else "250 mots max"
    cta_voice = "tutoie (tu/toi)" if platform.lower() == "instagram" else "vouvoie (vous)"

    user_prompt = (
        f"Crée un post organique pour {platform}.\n"
        f"Ton : {tone}\n"
        f"Audience : {audience}\n"
        f"Format : {content_format} (educational / reassurance / checklist)\n"
        f"Sujet : {topic}\n"
        f"Objectif : {objective}\n\n"
        f"Contraintes :\n"
        f"- Headline accrocheur (max 10 mots)\n"
        f"- Caption naturelle et humaine ({word_limit})\n"
        f"- CTA doux, sans pression, {cta_voice} l'audience\n\n"
        "Réponds uniquement avec un JSON valide avec les champs : headline, caption, cta"
    )

    client = anthropic.Anthropic()

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        final = stream.get_final_message()

    # Extract text block (skip thinking blocks)
    raw_text = next(
        block.text for block in final.content if block.type == "text"
    )

    # Strip markdown code fences if present
    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    content = json.loads(raw_text)

    return {
        "platform": platform,
        "type": "organic",
        "format": content_format,
        "rules": {
            "is_organic": True,
            "no_hard_sell": True,
            "no_urgency": True,
            "no_medical_absolutes": True,
            "voice": "Une infirmière qui parle à une famille (pas une publicité).",
            "tone": tone,
            "audience": audience,
        },
        "headline": content["headline"],
        "caption": content["caption"],
        "cta": content["cta"],
    }


def generate_images_with_kie(images_config: dict) -> list:
    """Generate images via the kie.ai API."""
    api_key = os.environ.get("KIE_API_KEY", "")
    if not api_key:
        raise ValueError("KIE_API_KEY environment variable not set")

    mode = images_config.get("mode", "txt2img")
    anchor_url = images_config.get("anchor_url", "")
    scenes = images_config.get("scenes", [])
    count = images_config.get("count", len(scenes) or 1)
    aspect_ratio = images_config.get("aspect_ratio", "1:1")
    style_rules = images_config.get("style_rules", "realistic, professional, clinical, warm, calm")
    quality = images_config.get("quality", "high")

    anchor_available = (
        mode == "img2img"
        and anchor_url
        and anchor_url != "PASTE_RAW_GITHUB_IMAGE_URL_HERE"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    scenes_to_generate = scenes[:count] if scenes else [f"Scene {i + 1}" for i in range(count)]
    result_urls = []

    for scene in scenes_to_generate:
        prompt = f"{scene}. Style: {style_rules}."
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "quality": quality,
        }
        if anchor_available:
            payload["image_url"] = anchor_url
            payload["mode"] = "img2img"
        else:
            payload["mode"] = "txt2img"

        resp = requests.post(
            "https://api.kie.ai/v1/images/generate",
            json=payload,
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

        url = (
            data.get("url")
            or data.get("image_url")
            or (data.get("output") or {}).get("url", "")
        )
        if url:
            result_urls.append(url)

    return result_urls


if __name__ == "__main__":
    brief = load_json("sample_brief.json")

    result = generate_organic_content(brief)

    if brief.get("images", {}).get("provider") == "kie.ai":
        urls = generate_images_with_kie(brief["images"])
        result["images"] = {
            "provider": "kie.ai",
            "result_urls": urls,
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))
