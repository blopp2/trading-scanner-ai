# Einstiegspunkt für das System
if __name__ == "__main__":
    print("Trading Scanner AI gestartet.")

import json
from core.process_response import process_gpt_result

# Beispiel: Ergebnis von GPT aus Datei laden (oder aus `gpt4_vision` direkt)
with open("output.json", "r") as f:
    gpt_data = json.load(f)

df = process_gpt_result(gpt_data)

print(df)
