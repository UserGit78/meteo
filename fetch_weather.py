"""Scarica il meteo attuale da Open-Meteo e lo aggiunge a data/meteo_loreto.csv.

Usa solo la libreria standard: nessuna dipendenza da installare.
"""
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

LAT, LON = 43.4400, 13.6100  # Loreto
CSV_PATH = Path("data/meteo_loreto.csv")
FIELDS = ["time", "temperature_2m", "relative_humidity_2m",
          "precipitation", "wind_speed_10m", "pressure_msl"]

params = {
    "latitude": LAT,
    "longitude": LON,
    "current": ",".join(FIELDS[1:]),
    "timezone": "Europe/Rome",
}
url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)

with urllib.request.urlopen(url, timeout=30) as resp:
    current = json.load(resp)["current"]

row = {k: current.get(k) for k in FIELDS}

CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
is_new = not CSV_PATH.exists()

# Evita duplicati se la rilevazione è già presente
if not is_new:
    with CSV_PATH.open(newline="") as f:
        if any(r["time"] == row["time"] for r in csv.DictReader(f)):
            print("Rilevazione già presente, nulla da aggiungere.")
            raise SystemExit(0)

with CSV_PATH.open("a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    if is_new:
        writer.writeheader()
    writer.writerow(row)

print("Aggiunta riga:", row)
