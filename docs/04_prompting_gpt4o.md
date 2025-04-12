# 🧠 Prompting für GPT-4o Vision

## 🎯 Ziel

Screenshots aus einem Trading-Scanner sollen automatisiert ausgewertet werden, um folgende Werte pro Zeile/Symbol zu extrahieren:

- Symbol
- ZENp
- AtrSprd
- AtrVWAP
- AtrHoD
- ZenV

Ziel ist es, die Daten maschinenlesbar als JSON weiterzuverarbeiten und mit einem Scoring-Modell zu bewerten.

---

## 📸 Haupt-Prompt an GPT-4o

```text
Extrahiere aus diesem Screenshot pro Zeile die folgenden Spalten:
Symbol, ZENp, AtrSprd, AtrVWAP, AtrHoD, ZenV

Gib das Ergebnis als JSON-Array zurück. Beispiel:

[
  {
    "Symbol": "SQQQ",
    "ZENp": "1.99",
    "AtrSprd": "2.05",
    "AtrVWAP": "1.46",
    "AtrHoD": "0.18",
    "ZenV": "13.42"
  },
  ...
]
```

---

## 🧾 Formatierungsregeln

- Ignoriere visuelle Trennlinien oder Icons
- Entferne Sonderzeichen wie `%`, `$`, `±` sofern vorhanden
- Erkenne auch Sonderwerte wie "∞" korrekt als Text

---

## 💬 Optionale Nachbearbeitung

Folgende Informationen können in einer zweiten Anfrage hinzugefügt werden:

- Bitte ignoriere Leerzeilen oder unvollständige Einträge
- Gib nur vollständig erkannte Zeilen aus

---

## 🌐 Verknüpfung zum Projekt

Das gesamte Projekt ist auf GitHub dokumentiert:

👉 [GitHub Repository: trading-scanner-ai](https://github.com/blopp2/trading-scanner-ai)

Dort findest du u. a.:

- Vision-Modul: `vision_engine/gpt4_vision.py`
- Bewertung & Scoring: `core/process_response.py`
- Scoring-Logik: `core/scoring.py`

---

Letztes Update: automatisch generiert am `2025-04-12`
