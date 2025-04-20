"""
Trading Scanner Controller

Dieses Programm ermöglicht es, einen Bereich des Bildschirms auszuwählen,
einen Screenshot dieses Bereichs aufzunehmen und über die ChatGPT-Vision-API
analysieren zu lassen.

Bedienung:
1. Starte das Programm: python scan_controller.py
2. Klicke auf "Region auswählen" und zeichne im erscheinenden Fenster
das rote Rechteck per Drag & Drop um den gewünschten Bildschirmausschnitt.
   - Bestätige die Auswahl mit Enter
3. Du erhältst eine Meldung, dass der Bereich gespeichert wurde.
4. Klicke auf "Region aktualisieren", wenn du einen neuen Bereich definieren willst.
5. Klicke auf "Screenshot & Analyse", um den gespeicherten Bereich zu capturen.
   - Der Screenshot wird als selected_region.png gespeichert.
   - Die Daten werden an die ChatGPT-API geschickt und die JSON-Antwort im
     großen Textfeld ausgegeben.

Voraussetzungen:
- Python 3.8+
- Installierte Pakete: pyautogui, pillow, numpy, opencv-python, openai, python-dotenv
- OpenAI-API-Key in .env-Datei: OPENAI_API_KEY=dein_schluessel

Dateien:
- area.json: speichert die zuletzt gewählte Region
- selected_region.png: temporärer Screenshot des Bereichs
- output.json: JSON-Antwort der API
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyautogui
from PIL import Image
import json
import numpy as np
import cv2
import os
from vision_engine.gpt4_vision import analyze_trading_scanner

# Pfad für area.json
AREA_FILE = "area.json"

class TradingScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Scanner Controller")
        self.region = self.load_region()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.select_btn = tk.Button(btn_frame, text="Region auswählen", command=self.select_region)
        self.select_btn.grid(row=0, column=0, padx=5)

        self.update_btn = tk.Button(btn_frame, text="Region aktualisieren", command=self.select_region)
        self.update_btn.grid(row=0, column=1, padx=5)

        self.capture_btn = tk.Button(btn_frame, text="Screenshot & Analyse", command=self.capture_and_analyze)
        self.capture_btn.grid(row=0, column=2, padx=5)

        # Label für Region
        self.region_label = tk.Label(root, text=self.region_text())
        self.region_label.pack(pady=5)

        # Textausgabe
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_text.pack(padx=10, pady=10)

    def region_text(self):
        if self.region:
            x, y, w, h = self.region
            return f"Aktueller Bereich: x={x}, y={y}, w={w}, h={h}"
        return "Kein Bereich ausgewählt."

    def load_region(self):
        if os.path.exists(AREA_FILE):
            with open(AREA_FILE, "r") as f:
                r = json.load(f)
                return r["x"], r["y"], r["w"], r["h"]
        return None

    def save_region(self, x, y, w, h):
        with open(AREA_FILE, "w") as f:
            json.dump({"x": x, "y": y, "w": w, "h": h}, f)
        self.region = (x, y, w, h)
        self.region_label.config(text=self.region_text())

    def select_region(self):
        # Screenshot
        full_img = pyautogui.screenshot()
        img_cv = cv2.cvtColor(np.array(full_img), cv2.COLOR_RGB2BGR)
        # ROI-Auswahl
        messagebox.showinfo("Region auswählen", "Ziehe nun den gewünschten Bereich im geöffneten Fenster und bestätige mit Enter.")
        x, y, w, h = cv2.selectROI("Select ROI", img_cv, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()
        if w > 0 and h > 0:
            self.save_region(int(x), int(y), int(w), int(h))
            messagebox.showinfo("Bereich gespeichert", f"x={x}, y={y}, w={w}, h={h}")
        else:
            messagebox.showwarning("Abgebrochen", "Keine Region ausgewählt.")

    def capture_and_analyze(self):
        if not self.region:
            messagebox.showerror("Fehler", "Bitte zuerst einen Bereich auswählen.")
            return
        x, y, w, h = self.region
        full_img = pyautogui.screenshot()
        region_img = full_img.crop((x, y, x+w, y+h))
        tmp_path = "selected_region.png"
        region_img.save(tmp_path)

        # API-Aufruf
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Analysiere...")
        self.root.update()
        try:
            analyze_trading_scanner(tmp_path)
            # Lade result.json und zeige Inhalt
            if os.path.exists("output.json"):
                with open("output.json", "r") as f:
                    data = json.load(f)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, json.dumps(data, indent=2))
            else:
                self.output_text.insert(tk.END, "Keine output.json gefunden.")
        except Exception as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Fehler bei Analyse: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingScannerGUI(root)
    root.mainloop()
