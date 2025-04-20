import click
import json
import os
from core.capture import select_region_opencv, capture_region
from core.vision import analyze_trading_scanner

AREA_FILE = "area.json"

@click.group()
def cli():
    """Trading Scanner AI CLI."""
    pass

@cli.command()
def select_region():
    """Interaktiv Region auswählen und speichern."""
    region = select_region_opencv()
    with open(AREA_FILE, 'w') as f:
        json.dump({'x': region[0], 'y': region[1], 'w': region[2], 'h': region[3]}, f)
    click.echo(f"Region gespeichert: {region}")

@cli.command()
def capture():
    """Screenshot der gespeicherten Region aufnehmen und analysieren."""
    if not os.path.exists(AREA_FILE):
        click.echo("Keine Region definiert. Bitte erst 'select-region' ausführen.")
        return
    with open(AREA_FILE) as f:
        r = json.load(f)
    img = capture_region((r['x'], r['y'], r['w'], r['h']))
    img.save('selected_region.png')
    click.echo("Screenshot gespeichert: selected_region.png")
    data = analyze_trading_scanner('selected_region.png')
    click.echo("Analyse abgeschlossen. Ausgabe:")
    click.echo(json.dumps(data, indent=2))

@cli.command()
def serve_gui():
    """Starte das GUI-Frontend."""
    import tkinter as tk
    from gui.controller import TradingScannerGUI
    root = tk.Tk()
    app = TradingScannerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    cli()
