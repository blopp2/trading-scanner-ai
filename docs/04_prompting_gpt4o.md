# 04_prompting_gpt4o.md

## 🎯 Ziel
Die GPT-4o Vision-Schnittstelle extrahiert strukturierte Trading-Daten aus Screenshots der Scanner-Oberfläche (z. B. TradingView oder Finviz).

---

## 📤 Prompt-Design für Bildauswertung
Die Vision-Komponente verwendet folgenden Prompt:

```text
Extrahiere aus dem Screenshot pro Zeile die folgenden Spalten:
Symbol, Price, Volume, ZenV, ZenP, AtrSprd, AtrVWAP, AtrHoD.
Gib ausschließlich ein korrekt formatiertes JSON-Array zurück.
Keine Kommentare, keine Erklärungen.
Beginne mit [ und schließe mit ].
```

Der Prompt wird zusammen mit dem Bild an `gpt-4o` gesendet. Die Bilddaten werden Base64-kodiert.

---

## 📥 GPT-Response: Parsing & Validierung
Das Modul `vision_engine/gpt4_vision.py` übernimmt folgende Schritte:

1. 🔍 **Antwort bereinigen**:
   - Entfernt ```json oder ```-Markdown-Blöcke
   - Strip & Clean

2. 🧠 **Parsing mit Fallback**:
   - Standard: `json.loads()`
   - Fallback: `literal_eval()` (z. B. bei unvollständigen Antworten)
   - Zeilenweises Parsen für Teilergebnisse, falls GPT-Output abgeschnitten ist

3. 🔧 **Normalisierung**:
   - `Price` → `Prize` (float)
   - `ZenP` → `ZENp` (float)
   - `Volume`: konvertiert Formate wie `4.5M`, `217K`, `1,000,000` in Integer

4. 💾 **Speicherung**:
   - `output.json` → für Weiterverarbeitung
   - `raw_gpt_response.txt` → Debug-Zwecke

---

## 🧾 Beispiel-Antwort (korrekt)
```json
[
  {"Symbol": "SQQQ", "Price": "55.09", "Volume": "6.8M", "ZenV": "13.42", "ZenP": "1.9", "AtrSprd": "2.08", "AtrVWAP": "0.62", "AtrHoD": "0.64"},
  {"Symbol": "SOXS", "Price": "49.04", "Volume": "4.7M", "ZenV": "14.06", "ZenP": "1.31", "AtrSprd": "4.57", "AtrVWAP": "2.65", "AtrHoD": "0.84"}
]
```

---

## ⚠️ Typische Fehler & Gegenmaßnahmen
| Problem                        | Lösung                                                   |
|-------------------------------|-----------------------------------------------------------|
| Unvollständiger JSON-Output   | Zeilenweises Reparatur-Parsing (abgeschlossene Objekte)   |
| Markdown-Wrapper (` ``` `)    | Automatisch entfernt vor Parsing                         |
| Volumen mit Suffix (z. B. M)  | Wird mit `parse_volume()` in Integer umgewandelt         |
| Falsche Feldnamen             | `Price`/`ZenP` werden umbenannt und gecastet             |

---

## 🔮 Erweiterungsideen
- Automatisches Screenshot-Watching mit OCR-Vorverarbeitung
- Auto-Retry bei GPT-Antwort < 3 Objekten
- Integration in Streamlit zur Live-Visualisierung

