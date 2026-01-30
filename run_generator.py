def generate_organic_content(brief: dict) -> dict:
    platform = (brief.get("platform") or "Facebook").strip()
    tone = brief.get("tone") or "Clinique, calme, humain, rassurant"
    audience = brief.get("audience") or "Familles"
    key_points = brief.get("key_points") or []

    # ORGANIC RULES (non-paid, non-salesy)
    rules = {
        "is_organic": True,
        "no_hard_sell": True,
        "no_urgency": True,
        "no_medical_absolutes": True,
        "voice": "Une infirmière qui parle à une famille (pas une publicité).",
        "tone": tone,
        "audience": audience,
    }

    # Pick a content format (rotate later if you want)
    # 1) Educational mini-post
    # 2) Reassurance/validation
    # 3) Checklist/actionable
    content_format = brief.get("format") or "educational"

    if content_format == "educational":
        headline = "3 signes que votre proche a besoin d’un peu plus de soutien à domicile"
        body = (
            "Parfois, ce n’est pas « une grosse urgence »… mais une accumulation.\n\n"
            "Voici 3 signes fréquents :\n"
            "1) La médication devient mêlante (doses oubliées, doubles prises)\n"
            "2) L’énergie diminue et les activités se réduisent\n"
            "3) Les proches commencent à s’épuiser\n\n"
            "👉 Le plus important : vous n’êtes pas seul(e). Un regard clinique à domicile aide souvent à clarifier quoi prioriser."
        )
        cta = "Si vous voulez, écrivez-moi « INFO » et je vous guide selon votre situation."
    elif content_format == "reassurance":
        headline = "Vous faites déjà beaucoup (et c’est normal de trouver ça lourd)"
        body = (
            "Être proche aidant, c’est porter beaucoup… souvent en silence.\n\n"
            "Si vous vous sentez dépassé(e), ce n’est pas un échec : "
            "c’est un signal que vous avez besoin de soutien, vous aussi.\n\n"
            "Un accompagnement infirmier à domicile peut aider à remettre de l’ordre, "
            "prévenir les visites à l’urgence et sécuriser la suite — étape par étape."
        )
        cta = "Vous pouvez m’écrire en privé. Je réponds avec douceur et sans pression."
    else:  # checklist/actionable
        headline = "Mini check-list (5 minutes) pour sécuriser le maintien à domicile"
        body = (
            "✔ Médication : liste à jour + pilulier + pharmacie\n"
            "✔ Chutes : tapis, éclairage, chaussures, aides techniques\n"
            "✔ Hydratation/alimentation : apports réels dans une journée\n"
            "✔ Plaies/peau : rougeurs, douleur, changements\n"
            "✔ Épuisement du proche : sommeil, pauses, relais\n\n"
            "Un petit ajustement peut faire une grande différence sur la sécurité à domicile."
        )
        cta = "Si vous voulez, dites-moi l’âge et la situation générale, je vous propose une piste."

    # Platform tweaks (FB tends to be longer + warmer; IG can be shorter)
    if platform.lower() == "instagram":
        body = body.replace("\n\n", "\n")  # tighter spacing
        cta = "DM-moi « INFO » si tu veux en parler."

    return {
        "platform": platform,
        "type": "organic",
        "format": content_format,
        "rules": rules,
        "headline": headline,
        "caption": body,
        "cta": cta
    }
