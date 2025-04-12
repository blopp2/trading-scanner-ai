import pandas as pd
from datetime import datetime
from core.scoring import calculate_score, calculate_long_score


def mark_significance(row, previous_vwap=None):
    """Kennzeichne jede Kennzahl entsprechend ihrer Wirkung im Scoring-Modell."""
    def score_zenp(x):
        return "+" if x < 4 else ("-" if x > 4 else "o")

    def score_atrsprd(x):
        return "+" if x < 5 else ("-" if x > 15 else "o")

    def score_atrvwap(x):
        return "+" if x > 0 else ("-" if x < 0 else "o")

    def score_atrhod(x):
        return "+" if x < 1 else ("-" if x > 5 else "o")

    def score_zenv(x):
        return "+" if x > 5 else ("-" if x < -2 else "o")

    def score_vwap_flip(current_vwap, previous_vwap):
        if previous_vwap is None:
            return "o"
        if previous_vwap < 0 < current_vwap:
            return "+"
        return "o"

    row["ZENp"] = f"{row['ZENp']:.2f}{score_zenp(row['ZENp'])}"
    row["AtrSprd"] = f"{row['AtrSprd']:.2f}{score_atrsprd(row['AtrSprd'])}"
    row["AtrVWAP"] = f"{row['AtrVWAP']:.2f}{score_atrvwap(row['AtrVWAP'])}"
    row["AtrHoD"] = f"{row['AtrHoD']:.2f}{score_atrhod(row['AtrHoD'])}"
    row["ZenV"] = f"{row['ZenV']:.2f}{score_zenv(row['ZenV'])}"
    row["VWAP_Flip"] = score_vwap_flip(row['AtrVWAP'], previous_vwap)

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

    # Long-optimierter Score
    df["LongScore"] = df.apply(
        lambda row: calculate_long_score(
            row, previous_vwap=previous_vwap_map.get(row["Symbol"])
        ),
        axis=1
    )

    # Werte markieren basierend auf Scoring-Logik
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
