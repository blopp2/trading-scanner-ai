import pytest
from core.scoring import score_zenp, score_atrsprd


def test_score_zenp():
    assert score_zenp(-3) == 1
    assert score_zenp(5) == -1
    assert score_zenp(0) == 0
