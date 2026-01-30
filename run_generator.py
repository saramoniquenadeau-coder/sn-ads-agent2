import json
from pathlib import Path

def generate_organic_content(brief: dict) -> dict:
    return {
        "platform": brief.get("platform"),
        "type": "organic",
        "headline": "Prendre soin à domicile, en toute confiance",
        "caption": "Un accompagnement infirmier humain et rassurant pour votre proche.",
        "cta": "Écrivez-nous pour en discuter"
    }

def main():
    brief = json.loads(Path("sample_brief.json").read_text(encoding="utf-8"))
    result = generate_organic_content(brief)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
