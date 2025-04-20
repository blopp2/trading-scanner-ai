# 06_to-do-roadmap.md

## ✅ Erledigt (Q1–Q2 2025)

### 🔍 GPT Vision Integration
- [x] GPT-4o eingebunden (Bild → JSON Parsing)
- [x] Volumen-Konvertierung (M, K, `,` → Integer)
- [x] Fallback-Parser für unvollständige GPT-Antworten
- [x] Feld-Normalisierung (`Price` → `Prize`, `ZenP` → `ZENp`)

### 📈 Scoring-System
- [x] Trennung zwischen `Score` und `LongScore`
- [x] Markierung visuell über `+`, `o`, `-` via Scoring-Logik
- [x] Modulare Bewertungsfunktionen in `scoring.py`
- [x] Spaltenformate `Prize_fmt`, `Volume_fmt`

### 📤 Output & Steuerung
- [x] Strukturierte Ausgabe mit Spaltenreihenfolge in `main.py`
- [x] Ausgabe als CSV und JSON
- [x] Timestamp in jeder Zeile

---

## 🧩 Offene To-Dos (Q2–Q3 2025)

### 🚀 Automatisierung
- [ ] Auto-Screenshot-Watching (Ordnerüberwachung, Trigger → Analyse)
- [ ] Batch-Modus für mehrere Screenshots (z. B. Tagesverlauf)
- [ ] Snapshot-Uhrzeit im Dateinamen erfassen / extrahieren

### 📊 UI/Visualisierung
- [ ] Streamlit-Frontend für Live-Scoring & Visualisierung
- [ ] Sortierbare Tabellen mit Filter (Score, Preis, Volumen)
- [ ] Score-Farbcodierung (Heatmap-Stil)

### 🧠 Datenquellen & Technik
- [ ] Integration von Live-VWAP/ATR-Daten aus API (z. B. Polygon, Finnhub)
- [ ] Berechnung von ZENp auf Basis echter VWAP (optional)
- [ ] Snapshot-Archivierung (JSON + PNG pro Analyse)

### 🛠️ TradingView-Kompatibilität
- [ ] Exportierbare Scanner-Profile (Premarket Movers)
- [ ] Automatischer Screenshot mit Hotkey oder Browser-Erweiterung
- [ ] Anbindung an Watchlists (via API oder manuell)

---

## ✨ Nice-to-Have Ideen
- Telegram-/Discord-Benachrichtigung bei Top-Scans
- Export nach Excel / Google Sheets
- Chart-Marker basierend auf Score direkt in TradingView (manuell oder Pine Script)
- Analyse von Aftermarket & Intraday-Daten (2 Modi)

---

## 🧭 Zielbild: „Scanner Copilot“
> Ein halbautomatischer Assistent, der Screenshots verarbeitet, bewertet und priorisierte Kandidaten liefert – inklusive Alerts, Visualisierung und Archivierung.