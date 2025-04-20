import pandas as pd
from datetime import datetime
from core.scoring import calculate_score, calculate_long_score, mark_significance

def clean_and_convert(value):
    """
    Versucht, einen gegebenen Wert in float zu konvertieren. Nicht numerische oder fehlende Werte werden zu 0.0.
    """
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            # Entferne nicht-numerische Zeichen
            cleaned = ''.join(ch for ch in value if (ch.isdigit() or ch in '.-'))
            try:
                return float(cleaned)
            except ValueError:
                return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def process_gpt_result(
    raw_data: list,
    previous_vwap_map: dict = None,
    filter_long_only: bool = False
) -> pd.DataFrame:
    """
    Verarbeitet das von GPT-4o extrahierte JSON-Array und berechnet Scores.

    Args:
        raw_data: Liste von Dictionaries mit Keys: Symbol, Prize, Volume, ZENp, AtrSprd, AtrVWAP, AtrHoD, ZenV
        previous_vwap_map: Optionales Mapping Symbol->vorheriger VWAP-Wert für Flip-Score
        filter_long_only: Wenn True, werden nur Zeilen mit LongScore >= 3 zurückgegeben

    Returns:
        pd.DataFrame mit den Originalwerten, Score-, LongScore- und timestamp-Spalten
    """
    # Erstelle DataFrame
    df = pd.DataFrame(raw_data)
    # Standardspalten sicherstellen
    for col in ["Prize", "Volume", "ZENp", "AtrSprd", "AtrVWAP", "AtrHoD", "ZenV"]:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = df[col].apply(clean_and_convert)

    # Scoring
    prev_map = previous_vwap_map or {}
    df["Score"] = df.apply(
        lambda row: calculate_score(row, previous_vwap=prev_map.get(row.get("Symbol"))),
        axis=1
    )
    df["LongScore"] = df.apply(
        lambda row: calculate_long_score(row, previous_vwap=prev_map.get(row.get("Symbol"))),
        axis=1
    )
    # Markiere signifikante Felder (optional fetten/annotieren)
    df = df.apply(
        lambda row: mark_significance(row, previous_vwap=prev_map.get(row.get("Symbol"))),
        axis=1
    )

    # Filter Long-Kandidaten
    if filter_long_only:
        df = df[df["LongScore"] >= 3]

    # Sortieren und Timestamp
    df = df.sort_values(by="LongScore", ascending=False).reset_index(drop=True)
    df["timestamp"] = datetime.now()
    return df
