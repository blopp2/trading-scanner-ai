from dotenv import load_dotenv
load_dotenv()
import os
import base64
from openai import OpenAI

client = OpenAI()

def encode_image(image_path):
    """Konvertiert ein Bild in base64-Format für die Vision-API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

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
                            "Analysiere diesen Screenshot eines Trading-Scanners. "
                            "Extrahiere pro Zeile: Symbol, ZENp, AtrSprd, AtrVWAP, AtrHoD, ZenV. "
                            "Gib das Ergebnis als JSON-Tabelle zurück."
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
        max_tokens=1000,
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    image_path = "scanner.png"  # Dein Screenshot hier
    result = analyze_trading_scanner(image_path)
    print("🧠 GPT-4o Vision Ergebnis:\n")
    print(result)
