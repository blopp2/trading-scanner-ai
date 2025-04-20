import os
import base64
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Lade Umgebungsvariablen (z.B. OPENAI_API_KEY)
load_dotenv()

# OpenAI-Client initialisieren
client = OpenAI()


def _encode_image(image_path: str) -> str:
    """
    Kodiert ein Bild als base64-String für die Vision-API.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def _parse_volume(volume_str: str) -> int:
    """
    Konvertiert Volumen-Angaben wie '1.2M', '800K', '1,234,567' in einen Integer.
    """
    if not isinstance(volume_str, str):
        return 0
    s = volume_str.replace(",", "").strip().upper()
    match = re.match(r"^([0-9]*\.?[0-9]+)([KMB]?)$", s)
    if not match:
        return 0
    num, suffix = match.groups()
    factor = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}.get(suffix, 1)
    return int(float(num) * factor)


def analyze_trading_scanner(image_path: str) -> list:
    """
    Sendet ein Trading-Scanner-Screenshot an GPT-4o Vision und gibt die extrahierten
    Daten als Liste von Dictionaries zurück. Speichert auch 'output.json' im CWD.
    """
    # Bild kodieren
    b64 = _encode_image(image_path)

    # Anfrage an GPT-4o Vision
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "You are a trading analyst. Extract structured data from this screenshot: "
                "Symbol, Price, Volume, ZenV, ZenP, AtrSprd, AtrVWAP, AtrHoD. "
                "Return a clean JSON array of objects."
            )},
            {"role": "user", "content": [
                {"type": "text", "text": ("Extract per line: Symbol, Price, Volume, "
                                            "ZenV, ZenP, AtrSprd, AtrVWAP, AtrHoD.")},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
            ]}
        ],
        max_tokens=3000,
    )
    raw = response.choices[0].message.content.strip()

    # Remove possible markdown wrapping
    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    elif raw.startswith("```"):
        raw = raw.replace("```", "").strip()

    # Parse JSON
    data = json.loads(raw)

    # Nachbearbeitung: Volumen parsen, Price -> Prize
    for entry in data:
        if "Volume" in entry:
            entry["Volume"] = _parse_volume(entry["Volume"])
        if "Price" in entry:
            entry["Prize"] = float(entry.pop("Price"))
        if "ZenP" in entry:
            entry["ZENp"] = float(entry.pop("ZenP"))

    # Schreibe Ergebnisdatei
    with open("output.json", "w") as f:
        json.dump(data, f, indent=2)

    return data
