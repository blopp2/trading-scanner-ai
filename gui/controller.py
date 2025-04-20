import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from core.capture import select_region_opencv, capture_region
from core.vision import analyze_trading_scanner
import json
import os

AREA_FILE = "area.json"

class TradingScannerGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Trading Scanner Controller")
        master.geometry('700x500')
        self.pack(fill='both', expand=True)
        self.region = self.load_region()
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)
        tk.Button(frame, text="Region auswählen", command=self.select_region).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Neuer Screenshot", command=self.capture_and_analyze).grid(row=0, column=1, padx=5)
        self.region_label = tk.Label(self, text=self.region_text())
        self.region_label.pack(pady=5)
        self.output = ScrolledText(self, width=60, height=15)
        self.output.pack(padx=10, pady=10)

    def region_text(self):
        if self.region:
            x, y, w, h = self.region
            return f"Bereich: x={x}, y={y}, w={w}, h={h}"
        return "Kein Bereich ausgewählt"

    def load_region(self):
        if os.path.exists(AREA_FILE):
            with open(AREA_FILE) as f:
                r = json.load(f)
            return r['x'], r['y'], r['w'], r['h']
        return None

    def save_region(self, x, y, w, h):
        with open(AREA_FILE, 'w') as f:
            json.dump({'x': x, 'y': y, 'w': w, 'h': h}, f)
        self.region = (x, y, w, h)
        self.region_label.config(text=self.region_text())

    def select_region(self):
        region = select_region_opencv()
        if region:
            x, y, w, h = region
            self.save_region(x, y, w, h)
        else:
            self.output.insert(tk.END, "Region-Auswahl abgebrochen.\n")

    def capture_and_analyze(self):
        if not self.region:
            self.output.insert(tk.END, "Bitte zuerst einen Bereich wählen.\n")
            return
        img = capture_region(self.region)
        img.save("selected_region.png")
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "Analysiere...\n")
        self.master.update()
        try:
            data = analyze_trading_scanner("selected_region.png")
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, json.dumps(data, indent=2) + "\n")
        except Exception as e:
            self.output.insert(tk.END, f"Fehler bei Analyse: {e}\n")
