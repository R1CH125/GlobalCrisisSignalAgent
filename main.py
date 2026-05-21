from __future__ import annotations

import argparse
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from backend.agent import CrisisSignalAgent
from backend.config import get_config

ROOT = Path(__file__).parent
FRONTEND_DIR = ROOT / "frontend"

config = get_config()
agent = CrisisSignalAgent(config)

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "mode": "demo" if config.demo_mode else "live"})


@app.get("/api/dashboard")
def dashboard():
    return jsonify(agent.dashboard_state())


@app.post("/api/run-once")
def run_once():
    return jsonify(agent.run_cycle())


@app.get("/api/cron")
def run_cron():
    return jsonify(agent.run_cycle())


@app.post("/api/demo")
def run_demo():
    return jsonify(agent.run_demo())


@app.get("/api/reports/latest")
def latest_report():
    reports = agent.dashboard_state()["reports"]
    return jsonify(reports[0] if reports else {})


@app.get("/components/<path:filename>")
def frontend_components(filename: str):
    return send_from_directory(FRONTEND_DIR / "components", filename)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Global Crisis Signal Agent")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5000, type=int)
    parser.add_argument("--run-once", action="store_true", help="Execute one monitoring cycle and print the JSON result.")
    parser.add_argument("--demo", action="store_true", help="Run the Northern Kenya drought demo and print the JSON result.")
    parser.add_argument("--no-monitor", action="store_true", help="Do not start the background monitoring loop.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.demo:
        print(agent.run_demo())
    elif args.run_once:
        print(agent.run_cycle())
    else:
        if not args.no_monitor:
            agent.start_monitoring()
        app.run(host=args.host, port=args.port, debug=False)
