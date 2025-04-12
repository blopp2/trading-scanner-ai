def score_zenp(x):
    if x > 4:
        return -1
    elif x < -2:
        return 1
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
    elif abs(x) > 2:
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

def score_vwap_flip(current_vwap, previous_vwap):
    if previous_vwap is None:
        return 0
    if previous_vwap < 0 and current_vwap > 0:
        return 1
    return 0

def calculate_score(row, previous_vwap=None):
    # Klassisches Score-Modell (Long/Short neutral)
    score = (
        score_zenp(row["ZENp"]) +
        score_atrsprd(row["AtrSprd"]) +
        score_atrvwap(row["AtrVWAP"]) +
        score_atrhod(row["AtrHoD"]) +
        score_zenv(row["ZenV"])
    )
    score += score_vwap_flip(row["AtrVWAP"], previous_vwap)
    return score

def calculate_long_score(row, previous_vwap=None):
    # Long-optimiertes Modell
    score = 0
    if previous_vwap is not None and previous_vwap < 0 < row["AtrVWAP"]:
        score += 1
    if row["ZenV"] > 5:
        score += 1
    if row["AtrVWAP"] < 0:
        score -= 1
    if row["AtrHoD"] < 1:
        score += 1
    if row["AtrSprd"] < 5:
        score += 1
    if row["ZENp"] < 4:
        score += 1
    return score
