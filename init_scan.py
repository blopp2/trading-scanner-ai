import pyautogui
from PIL import Image, ImageDraw
import pytesseract
import json
from pytesseract import Output

# Schritt 1: Screenshot vom gesamten Bildschirm machen
img = pyautogui.screenshot()
img.save("full_screen.png")

# Schritt 2: OCR auf Screenshot anwenden
data = pytesseract.image_to_data(img, output_type=Output.DICT)

# Schritt 3: Suche nach dem Wort "Momentum"
found = False
highlight_img = img.copy()
draw = ImageDraw.Draw(highlight_img)

for i, word in enumerate(data["text"]):
    if word.isupper() and 1 <= len(word) <= 5 and word.isalpha():
        # erweiterte Region um Symbol-Treffer
        x = data["left"][i]
        y = max(0, data["top"][i] - 40)   # 40 px nach oben
        w = 500                           # breite bis AtrHoD
        h = 280                           # hoch genug für alle Zeilen

        # Bereich speichern
        with open("area.json", "w") as f:
            json.dump({"x": x, "y": y, "w": w, "h": h}, f)

        print(f"✅ Bereich erkannt bei: x={x}, y={y}, w={w}, h={h}")

        # Highlight zur Kontrolle zeichnen
        draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
        highlight_img.save("ocr_debug.png")
        print("🔍 Vorschau gespeichert als ocr_debug.png")

        found = True
        break

if not found:
    print("❌ Bereich 'Momentum' nicht gefunden. Bitte Screenshot prüfen.")
