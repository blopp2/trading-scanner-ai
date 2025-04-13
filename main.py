# main.py
# Einstiegspunkt für das System
if __name__ == "__main__":
    print("Trading Scanner AI gestartet.")

import json
import pandas as pd
from core.process_response import process_gpt_result

# Pandas-Option: alle Spalten anzeigen
#pd.set_option("display.max_columns", None)

# Beispiel: Ergebnis von GPT aus Datei laden
with open("output.json", "r") as f:
    gpt_data = json.load(f)

# Verarbeitung
df = process_gpt_result(gpt_data)

# Definierte Spaltenreihenfolge (nur vorhandene Spalten übernehmen)
columns_order = [
    "Symbol", "Prize", "Volume_fmt", "ZenV", "ZENp", "AtrSprd", "AtrVWAP", "AtrHoD",
    "Score", "LongScore"
]
columns_to_show = [col for col in columns_order if col in df.columns]

# Ausgabe
print(df[columns_to_show])

# Speichern als JSON und CSV
df[columns_to_show].to_json("result.json", orient="records", indent=2)
df[columns_to_show].to_csv("result.csv", index=False)

print("Ergebnisse gespeichert: result.json & result.csv")
