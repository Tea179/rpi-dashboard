"""
RPi Dashboard – lekki panel monitorujący dla Raspberry Pi.
Serwuje stronę HTML oraz endpoint JSON /api/stats z bieżącymi statystykami.
"""

from flask import Flask, jsonify, render_template
import psutil
import socket
import time

app = Flask(__name__)

# Pierwsze wywołanie cpu_percent() zawsze zwraca wartość bez znaczenia
# (brak punktu odniesienia) – wywołujemy je raz przy starcie, żeby je odrzucić.
psutil.cpu_percent(interval=None)

THERMAL_ZONE = "/sys/class/thermal/thermal_zone0/temp"


def get_cpu_temp():
    """Odczytuje temperaturę SoC. Zwraca None, jeśli plik nie istnieje (np. nie na RPi)."""
    try:
        with open(THERMAL_ZONE, "r") as f:
            return round(int(f.read().strip()) / 1000.0, 1)
    except (FileNotFoundError, ValueError, PermissionError):
        return None


def format_uptime(seconds):
    days, rem = divmod(int(seconds), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if days or hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def stats():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    try:
        load1, load5, load15 = psutil.getloadavg()
    except (AttributeError, OSError):
        load1 = load5 = load15 = 0.0

    return jsonify(
        {
            "hostname": socket.gethostname(),
            "temperature_c": get_cpu_temp(),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "load_avg": [round(load1, 2), round(load5, 2), round(load15, 2)],
            "uptime": format_uptime(time.time() - psutil.boot_time()),
            "memory": {
                "total": mem.total,
                "free": mem.available,
                "percent_used": mem.percent,
            },
            "disk": {
                "total": disk.total,
                "free": disk.free,
                "percent_used": round(disk.used / disk.total * 100, 1),
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
