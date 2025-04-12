# 📊 Scoring-System

## Bewertungslogik (einfaches Modell)

| Kennzahl  | Regel                    | Punkte |
| --------- | ------------------------ | ------ |
| ZENp      | > 4 = -1, < -2 = +1      | ±1     |
| AtrSprd   | < 3 = +1, > 15 = -1      | ±1     |
| AtrVWAP   | < 1 = +1, > 2 = -1       | ±1     |
| AtrHoD    | < 1 = +1, > 5 = -1       | ±1     |
| ZenV      | > 5 = +1, < -2 = -1      | ±1     |
| VWAP-Flip | prev < 0 & curr > 0 = +1 | +1     |

## Interpretation

- +3 bis +5 → 🔥 Long-Kandidat
- 0 bis +2 → 🟡 Beobachtung
- < 0 → 🔻 Schwach
