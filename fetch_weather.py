"""Scarica il riepilogo meteo del giorno precedente (Loreto) da Open-Meteo
e lo aggiunge a data/meteo_loreto_giornaliero.csv.

Si registra "ieri" perché è una giornata completa: minima, massima e
pioggia totale sono definitive. Usa solo la libreria standard.
"""
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

LAT, LON = 43.4400, 13.6100  # Loreto
CSV_PATH = Path("data/meteo_loreto_giornaliero.csv")
DAILY = ["temperature_2m_max", "temperature_2m_min",
         "precipitation_sum", "wind_speed_10m_max"]
FIELDS = ["date"] + DAILY

params = {
    "latitude": LAT,
    "longitude": LON,
    "daily": ",".join(DAILY),
    "past_days": 1,       # include ieri
    "forecast_days": 1,   # più oggi (non usato)
    "timezone": "Europe/Rome",
}
url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)

with urllib.request.urlopen(url, timeout=30) as resp:
    daily = json.load(resp)["daily"]

# L'indice 0 è ieri, l'indice 1 è oggi
row = {"date": daily["time"][0]}
for key in DAILY:
    row[key] = daily[key][0]

CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
is_new = not CSV_PATH.exists()

# Evita duplicati se il giorno è già presente
if not is_new:
    with CSV_PATH.open(newline="") as f:
        if any(r["date"] == row["date"] for r in csv.DictReader(f)):
            print("Giorno già presente, nulla da aggiungere.")
            raise SystemExit(0)

with CSV_PATH.open("a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    if is_new:
        writer.writeheader()
    writer.writerow(row)

print("Aggiunta riga:", row)
