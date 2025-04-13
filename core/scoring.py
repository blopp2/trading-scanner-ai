# core/scoring.py

def score_zenp(x):
    if x < -2:
        return 1
    elif x > 4:
        return -1
    return 0

def score_atrsprd(x):
    if x < 3:
        return 1
    elif x > 15:
        return -1
    return 0

def score_atrvwap(x):
    if abs(x) < 1:
        return 1
    elif abs(x) > 5:
        return -1
    return 0

def score_atrhod(x):
    if x < 1:
        return 1
    elif x > 5:
        return -1
    return 0

def score_zenv(x):
    if x > 5:
        return 1
    elif x < -2:
        return -1
    return 0

def score_vwap_flip(current, previous):
    if previous is not None and previous < 0 < current:
        return 1
    return 0

def calculate_score(row, previous_vwap=None):
    return (
        score_zenp(row["ZENp"]) +
        score_atrsprd(row["AtrSprd"]) +
        score_atrvwap(row["AtrVWAP"]) +
        score_atrhod(row["AtrHoD"]) +
        score_zenv(row["ZenV"]) +
        score_vwap_flip(row["AtrVWAP"], previous_vwap)
    )

def calculate_long_score(row, previous_vwap=None):
    score = 0
    if row["ZENp"] < 4:
        score += 1
    if row["AtrSprd"] < 5:
        score += 1
    if row["AtrVWAP"] > 0:
        score += 1
    if row["AtrHoD"] < 1:
        score += 1
    if row["ZenV"] > 5:
        score += 1
    if previous_vwap is not None and previous_vwap < 0 < row["AtrVWAP"]:
        score += 1
    return score

def mark_field(score_func, value, *args):
    if score_func is None:
        return value  # Gib den Originalwert zurück, ohne Kennzeichnung
    score = score_func(value, *args) if args else score_func(value)
    if score > 0:
        return f"{value:.2f}+"
    elif score < 0:
        return f"{value:.2f}-"
    return f"{value:.2f}o"

def mark_significance(row, previous_vwap=None):
    row["Prize"] = float(row.get("Prize", 0))
    row["Volume"] = float(row.get("Volume", 0))

    row["ZENp"]    = mark_field(score_zenp, row["ZENp"])
    row["AtrSprd"] = mark_field(score_atrsprd, row["AtrSprd"])
    row["AtrVWAP"] = mark_field(score_atrvwap, row["AtrVWAP"])
    row["AtrHoD"]  = mark_field(score_atrhod, row["AtrHoD"])
    row["ZenV"]    = mark_field(score_zenv, row["ZenV"])

    # Formatierte Ausgabe ohne Kennzeichnung
    row["Prize_fmt"]  = f"{row['Prize']:.2f}"
    row["Volume_fmt"] = f"{row['Volume']:.0f}"

    return row
