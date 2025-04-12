#!/bin/bash

echo "📁 Erstelle Projektstruktur..."

# Verzeichnisse
mkdir -p vision_engine core overlay ui analytics config docs

# Basisdateien
echo '# 📊 Trading Scanner AI
Ein System zur Analyse und Bewertung von Trading-Screenshots basierend auf GPT-4o und technischen Kennzahlen.' > README.md

echo 'openai
pandas
pillow
opencv-python
easyocr
pyautogui
streamlit' > requirements.txt

echo '# Einstiegspunkt für das System
if __name__ == "__main__":
    print("Trading Scanner AI gestartet.")' > main.py

# Markdown-Dokumentation
cat <<EOT > docs/01_architekturuebersicht.md
# 🧠 Architekturübersicht – Trading-Scanner Analyse

## 🎯 Ziel des Systems
Ein Tool zur Analyse von Screenshots eines Trading-Scanners (z. B. aus YouTube-Livestreams), um Kennzahlen wie ZENp, AtrVWAP etc. zu extrahieren, zu bewerten und visuell darzustellen.

## 📐 Architekturdiagramm (vereinfacht)
\`\`\`mermaid
flowchart TD
    A[Screenshot / Stream] --> B[Vision & OCR]
    B --> C[Tabellenstruktur erkennen]
    C --> D[Scoring-Modul]
    D --> E[Overlay / GUI]
    D --> F[Logging & Alerts]
\`\`\`
EOT

# Weitere Beispiel-Dateien kannst du ergänzen wie oben

echo "✅ Projektstruktur erstellt!"
