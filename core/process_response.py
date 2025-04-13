# core/process_response.py
import pandas as pd
from datetime import datetime
from core.scoring import calculate_score, calculate_long_score, mark_significance

def clean_and_convert(x):
    if isinstance(x, str):
        x = x.replace("∞", "inf").replace("-", "0")
    try:
        return float(x)
    except:
        return 0.0

def process_gpt_result(json_data, previous_vwap_map=None, filter_long_only=False):
    df = pd.DataFrame(json_data)

    for col in ["Prize", "Volume", "ZENp", "AtrSprd", "AtrVWAP", "AtrHoD", "ZenV"]:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = df[col].map(clean_and_convert)

    previous_vwap_map = previous_vwap_map or {}

    df["Score"] = df.apply(
        lambda row: calculate_score(
            row, previous_vwap=previous_vwap_map.get(row["Symbol"])
        ),
        axis=1
    )

    df["LongScore"] = df.apply(
        lambda row: calculate_long_score(
            row, previous_vwap=previous_vwap_map.get(row["Symbol"])
        ),
        axis=1
    )

    df = df.apply(
        lambda row: mark_significance(
            row, previous_vwap=previous_vwap_map.get(row["Symbol"])
        ),
        axis=1
    )

    if filter_long_only:
        df = df[df["LongScore"] >= 3]

    df = df.sort_values(by="LongScore", ascending=False).reset_index(drop=True)
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return df
