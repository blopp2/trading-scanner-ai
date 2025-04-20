import pytest
from core.capture import capture_region, select_region_opencv
from PIL import Image


def test_capture_region(tmp_path, monkeypatch):
    # Mock pyautogui.screenshot
    dummy = Image.new('RGB', (100,100), color='white')
    monkeypatch.setattr('core.capture.pyautogui.screenshot', lambda region=None: dummy)
    img = capture_region((0,0,50,50))
    assert isinstance(img, Image.Image)
