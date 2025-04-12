# 🧭 Git Workflow für Trading-Scanner-AI

## 📦 Projekt-Versionierung mit Git

Dieses Projekt verwendet **Git** zur lokalen Versionsverwaltung und **GitHub** als zentrales Repository.

---

## 🔁 Standard-Ablauf

```bash
# 1. Änderungen anzeigen lassen
$ git status

# 2. Dateien zum Commit vormerken
$ git add .

# 3. Änderung lokal speichern (commit)
$ git commit -m "💡 Kurze Beschreibung der Änderung"

# 4. Lokale Commits nach GitHub senden (push)
$ git push
```

---

## 💬 Beispiele für Commit-Nachrichten

```bash
# Neue Datei hinzugefügt
$ git commit -m "🧠 Add: Prompt-Dokumentation für GPT-4o"

# Fehler behoben
$ git commit -m "🐛 Fix: falsche Bewertung in LongScore korrigiert"

# Visualisierung ergänzt
$ git commit -m "✨ Neu: Overlay mit Score-Anzeige implementiert"
```

---

## 🌐 GitHub-URL (Remote Repository)

[github.com/blopp2/trading-scanner-ai](https://github.com/blopp2/trading-scanner-ai)

Dort liegt das offizielle Hauptprojekt.

---

## 🧠 Tipp

- Erstelle oft kleine Commits mit klaren Nachrichten
- `git log` zeigt dir deine Commit-Historie
- Verzweigungen (`branches`) erlauben Feature-Tests ohne Risiko

---

Letztes Update: automatisch erstellt am `2025-04-12`
