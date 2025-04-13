# vision_engine/gpt4_vision.py

from dotenv import load_dotenv
load_dotenv()
import os
import base64
import json
import re
from openai import OpenAI

client = OpenAI()

def encode_image(image_path):
    """Konvertiert ein Bild in base64-Format für die Vision-API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def parse_volume(volume_str):
    """Konvertiert Volumen-Angabe wie '1.2M', '800K', '1,234,567' in int."""
    if not isinstance(volume_str, str):
        return 0
    volume_str = volume_str.replace(",", "").strip().upper()
    match = re.match(r"([0-9.]+)([KMB]?)", volume_str)
    if not match:
        return 0
    number, suffix = match.groups()
    factor = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}.get(suffix, 1)
    return int(float(number) * factor)

def analyze_trading_scanner(image_path):
    """Sendet ein Bild an GPT-4o zur Extraktion von Trading-Daten."""
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Du bist ein Trading-Analyst und extrahierst strukturierte Daten aus Screenshots."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extrahiere aus dem Screenshot pro Zeile die folgenden Spalten: "
                            "Symbol, Price, Volume, ZenV, ZenP, AtrSprd, AtrVWAP, AtrHoD. "
                            "Gib ausschließlich ein korrekt formatiertes JSON-Array zurück."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ],
            }
        ],
        max_tokens=3000,
    )

    result_text = response.choices[0].message.content.strip()

    # Entferne mögliche Markdown-Hüllen wie ```json ... ```
    if result_text.startswith("```json"):
        result_text = result_text.replace("```json", "").replace("```", "").strip()
    elif result_text.startswith("```"):
        result_text = result_text.replace("```", "").strip()

    with open("raw_gpt_response.txt", "w") as f:
        f.write(result_text)

    try:
        result_data = json.loads(result_text)
        print(f"✅ {len(result_data)} Einträge erfolgreich geladen.")
    except json.JSONDecodeError as e:
        print("❌ JSON-Parsing gescheitert:", e)
        print("Antworttext:")
        print(result_text)
        return

    for row in result_data:
        if "Volume" in row:
            row["Volume"] = parse_volume(row["Volume"])
        if "Price" in row:
            row["Prize"] = float(row["Price"])
        if "ZenP" in row:
            row["ZENp"] = float(row["ZenP"])

        row.pop("Price", None)
        row.pop("ZenP", None)

    with open("output.json", "w") as f:
        json.dump(result_data, f, indent=2)

    print("✅ Daten erfolgreich in output.json gespeichert.")

if __name__ == "__main__":
    image_path = "scanner.png"
    analyze_trading_scanner(image_path)
