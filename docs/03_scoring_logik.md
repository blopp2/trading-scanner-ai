# 03_scoring_logik.md

## 🎯 Ziel des Scoring-Moduls
Das Scoring-Modul bewertet die aus Screenshots extrahierten Trading-Kandidaten auf Basis technischer Kriterien. Die Bewertung erfolgt sowohl quantitativ (Score) als auch qualitativ visuell (Markierung).

---

## 🔍 Eingabedaten
Die Daten stammen aus der Vision-Auswertung (z. B. `output.json`) und enthalten pro Zeile folgende Felder:

| Feld        | Beschreibung                            |
|-------------|------------------------------------------|
| `Symbol`    | Tickersymbol                            |
| `Prize`     | Aktueller Kurs                          |
| `Volume`    | Premarket-Volumen (bereinigt)           |
| `ZenV`      | Volumen-Z-Score                         |
| `ZENp`      | Preisabweichung in ATR-Einheiten        |
| `AtrSprd`   | Spread in ATR-Einheiten                 |
| `AtrVWAP`   | Abweichung vom VWAP in ATR              |
| `AtrHoD`    | Abweichung vom Tageshoch in ATR         |

Diese Felder bilden die Grundlage für die Bewertungsfunktionen.

---

## 🧠 Bewertungslogik: `calculate_score()`
Der **klassische Score** berechnet positive und negative Signale:

```python
+1 wenn ZenV > 5
+1 wenn ZENp < 3
+1 wenn AtrVWAP > 0
+1 wenn AtrHoD < 1
-1 wenn ZenV < -2
-1 wenn ZENp > 6
-1 wenn AtrVWAP < 0
-1 wenn AtrHoD > 3
```

Resultat: Ein Score zwischen **-4 bis +4**

---

## ✅ LongScore: Nur positiv interpretierbare Kriterien

```python
+1 wenn ZENp < 4
+1 wenn AtrSprd < 5
+1 wenn AtrVWAP > 0
+1 wenn AtrHoD < 1
+1 wenn ZenV > 5
```
→ Ziel: Long-Kandidaten mit mind. 3 Punkten herausfiltern

---

## 🖍️ Markierung der Spalten für visuelle Ausgabe
Markierungen basieren auf den obigen Score-Funktionen und zeigen, **welche Kriterien erfüllt wurden**:

| Symbol | Bedeutung |
|--------|-----------|
| `+`    | erfüllt (`True`) für LongScore          |
| `o`    | neutral / kein Score-Kriterium          |
| `-`    | negativ im klassischen Score (nur optisch)

**Beispiel:**
- `ZENp = 1.31` → `1.31+`
- `AtrHoD = 0.84` → `0.84+`
- `ZenV = -14.06` → `-14.06-`

---

## 🧾 Technische Umsetzung
Die Bewertungen und Markierungen erfolgen in:
- `core/scoring.py` → Enthält `calculate_score`, `calculate_long_score`, `mark_significance`
- `core/process_response.py` → ruft Scoring-Funktionen auf und bereitet DataFrame für Anzeige & Export auf

---

## 📦 Ausgabe
Nach Anwendung der Bewertung enthält der DataFrame:
- berechnete Spalten: `Score`, `LongScore`
- formatierte Spalten: `ZENp`, `ZenV`, `AtrSprd`, ... mit Markierungen
- zusätzlich: `timestamp`, `Prize_fmt`, `Volume_fmt`

Die Ausgabe erfolgt über `main.py` in `result.json` und `result.csv`

---

## 🔮 Nächste Schritte (geplant)
- Score-Visualisierung (z. B. Farbskalen)
- Integration von ATR- oder VWAP-Historie aus externen Datenquellen
- Automatisches Markieren von Top-Kandidaten

