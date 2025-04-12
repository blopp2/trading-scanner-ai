import pandas as pd
from datetime import datetime
from core.scoring import calculate_score, calculate_long_score


def mark_significance(row, previous_vwap=None):
    """Kennzeichne nur Felder, die im LongScore explizit positiv gewertet wurden."""
    marks = {k: "o" for k in ["ZENp", "AtrSprd", "AtrVWAP", "AtrHoD", "ZenV"]}

    # Beispielhafte LongScore-Logik, analog zu bereinigtem calculate_long_score
    if row["ZENp"] < 4:
        marks["ZENp"] = "+"
    if row["AtrSprd"] < 5:
        marks["AtrSprd"] = "+"
    if row["AtrVWAP"] > 0:
        marks["AtrVWAP"] = "+"
    if row["AtrHoD"] < 1:
        marks["AtrHoD"] = "+"
    if row["ZenV"] > 5:
        marks["ZenV"] = "+"

    row["ZENp"] = f"{row['ZENp']:.2f}{marks['ZENp']}"
    row["AtrSprd"] = f"{row['AtrSprd']:.2f}{marks['AtrSprd']}"
    row["AtrVWAP"] = f"{row['AtrVWAP']:.2f}{marks['AtrVWAP']}"
    row["AtrHoD"] = f"{row['AtrHoD']:.2f}{marks['AtrHoD']}"
    row["ZenV"] = f"{row['ZenV']:.2f}{marks['ZenV']}"

    return row


def process_gpt_result(json_data, previous_vwap_map=None, filter_long_only=False):
    df = pd.DataFrame(json_data)

    # Konvertiere Strings in Float, inkl. "∞"
    for col in ["ZENp", "AtrSprd", "AtrVWAP", "AtrHoD", "ZenV"]:
        df[col] = df[col].replace("∞", float("inf")).astype(float)

    previous_vwap_map = previous_vwap_map or {}

    # Klassischer Score (Momentum-basiert)
    df["Score"] = df.apply(
        lambda row: calculate_score(
            row, previous_vwap=previous_vwap_map.get(row["Symbol"])
        ),
        axis=1
    )

    # Long-optimierter Score (nur positive Bedingungen)
    df["LongScore"] = df.apply(
        lambda row: (
            (1 if row["ZENp"] < 4 else 0) +
            (1 if row["AtrSprd"] < 5 else 0) +
            (1 if row["AtrVWAP"] > 0 else 0) +
            (1 if row["AtrHoD"] < 1 else 0) +
            (1 if row["ZenV"] > 5 else 0)
        ),
        axis=1
    )

    # Werte markieren basierend auf LongScore-Logik
    df = df.apply(
        lambda row: mark_significance(
            row, previous_vwap=previous_vwap_map.get(row["Symbol"])
        ),
        axis=1
    )

    # Optional: nur Long-Kandidaten anzeigen
    if filter_long_only:
        df = df[df["LongScore"] >= 3]

    # Nach LongScore sortieren
    df = df.sort_values(by="LongScore", ascending=False).reset_index(drop=True)

    # Zeitstempel hinzufügen
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return df
