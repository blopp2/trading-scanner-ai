# 🗺️ To-Do & Roadmap

Diese Roadmap zeigt den aktuellen Projektstatus und geplante Schritte für die nächsten Entwicklungsphasen.

---

## ✅ Abgeschlossen

- Projektstruktur & GitHub-Repo eingerichtet
- Architekturübersicht dokumentiert
- Scoring-Modell definiert (ZENp, VWAP, Spread etc.)
- `setup.sh` zur Projektinitialisierung erstellt
- Markdown-basierte Projektdokumentation integriert

---

## 🛠️ In Arbeit

### 🔍 GPT-4o Vision Integration

- [ ] Screenshot-Input vorbereiten (PNG/JPG)
- [ ] Prompt-Template erstellen
- [ ] Antwort strukturieren (Tabellen-JSON oder CSV)
- [ ] Vision-Auswertung testen (Beispiel-Screenshot FMTO)

### 🎨 Overlay-System

- [ ] Overlay-Modul mit Pillow oder OpenCV
- [ ] Farbcode basierend auf Score
- [ ] Positionierung anhand von Symbolzeilen
- [ ] Exportiertes Bild mit Score-Annotation

---

## 🧭 Geplant (Priorität A – Funktionalität)

### 🚀 Live-Aktualisierung

- [ ] Automatisches Screenshot-Polling (alle X Sekunden)
- [ ] Watcher-Modul für Scans
- [ ] Wechselerkennung im Stream (Neues Symbol im Fokus)

### 🔔 Alerts & Reaktionen

- [ ] VWAP-Flip erkennen & loggen
- [ ] Audio-/Popup-Alert bei starkem Setup (+3 oder mehr)
- [ ] E-Mail/Discord/Telegram-Integration (optional)

---

## 📊 Geplant (Priorität B – Analyse & UI)

### 📈 Visualisierung & UI

- [ ] Streamlit- oder Tkinter-Interface mit Bewertungsliste
- [ ] Ranking-Tabelle mit Filteroptionen (Score ≥ X)
- [ ] Heatmap pro Score-Bereich (Farbe nach Stärke)

### 🧠 Scoring-Verlauf & Historie

- [ ] Scoring-History pro Symbol speichern (CSV)
- [ ] Nachträgliche Erfolgskontrolle (Kurs vs Score)
- [ ] Backtest-Modul: Welche Scores führen zu Erfolgen?

---

## 🧪 Visionen für später

- [ ] Automatischer Screener (YouTube OCR Livestream)
- [ ] API-Anbindung an Broker (Paper-Trading?)
- [ ] Training eines Custom-Modells für Setup-Klassifizierung

---

## 📍 Nächster Fokus (Sprint 1)

1. GPT-4o Vision-Pipeline zum Laufen bringen
2. Overlay für Scores pro Symbol auf Screenshot
3. Erste Live-Testung mit regelmäßigem Screenshot
