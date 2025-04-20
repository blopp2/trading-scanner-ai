import numpy as np
import pyautogui
import cv2
from PIL import Image, ImageGrab

"""
Core Module für Region-Auswahl und Screenshot-Erstellung
"""


def select_region_opencv():
    """
    Öffnet ein OpenCV-Fenster zur interaktiven Auswahl eines Bildschirmbereichs (ROI)
    und gibt die Koordinaten (x, y, Breite, Höhe) als Integer zurück.
    """
    # Vollbild-Screenshot als PIL.Image
    screenshot = pyautogui.screenshot()
    # Umwandeln in OpenCV-Format
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # ROI-Auswahl durch den Nutzer
    x, y, w, h = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    return int(x), int(y), int(w), int(h)


def capture_region(region):
    """
    Nimmt von dem übergebenen Bereich einen Screenshot und liefert ihn als PIL.Image zurück.

    Args:
        region: Tuple (x, y, Breite, Höhe)

    Returns:
        PIL.Image des ausgewählten Bildschirmabschnitts durch Zuschneiden des Fullscreen-Screenshot.
    """
    # Screenshot der gesamten Anzeige
    full_img = pyautogui.screenshot()
    x, y, w, h = region
    # Zuschneiden des Screenshots
    return full_img.crop((x, y, x + w, y + h))
