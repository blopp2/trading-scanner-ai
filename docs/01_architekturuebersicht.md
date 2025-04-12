# 🧠 Architekturübersicht – Trading-Scanner Analyse

## 🎯 Ziel

Ein Tool zur Analyse von Screenshots eines Trading-Scanners, das technische Kennzahlen wie ZENp, AtrVWAP, AtrHoD etc. automatisch extrahiert, bewertet und visuell anzeigt.

## 📐 Architektur (vereinfacht)

```mermaid
flowchart TD
    A[Screenshot / Stream] --> B[Vision & OCR]
    B --> C[Tabellenstruktur erkennen]
    C --> D[Scoring-Modul]
    D --> E[Overlay / UI]
    D --> F[Logging & Alerts]
```
