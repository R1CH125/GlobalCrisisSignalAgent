# Global Crisis Signal Agent

An AI early warning system for humanitarian crises.

## Problem

Humanitarian crises often become visible to institutions only after multiple warning signs have already converged: drought signals, local social reporting, migration chatter, food market stress, and regional news coverage. Analysts lose time when those signals stay fragmented across APIs and dashboards.

## Solution

Global Crisis Signal Agent ingests social, news, and environmental data streams, normalizes them into one schema, detects anomalies, synthesizes the evidence with a Nemotron-style reasoning layer, computes a weighted crisis likelihood score, and dispatches alerts while updating a live dashboard.

The prototype is designed for hackathon demo value:

- It runs immediately in `DEMO_MODE=true` with a realistic Northern Kenya drought scenario.
- It switches to live API ingestion when credentials are present.
- It includes alert payloads for ReliefWeb, Slack, Discord, AWS SES, and generic NGO webhooks.

## Architecture

```text
APIs -> Source Clients -> Unified Signal Schema -> Cleaning Pipeline
    -> Indicator Extraction -> Historical Similarity -> Nemotron Reasoning
    -> Crisis Score Engine -> Alert Dispatcher -> Flask API -> Dashboard
```

### Core flow

1. Collect real-time signals from social, news, and environmental sources.
2. Clean and deduplicate the signal stream.
3. Detect spikes, multi-source confirmation, geographic clustering, and environmental correlation.
4. Run structured Nemotron-style reasoning.
5. Compute a crisis score with the weighted formula below.
6. Trigger alerts and update the dashboard.

## APIs Used

### Social

- Twitter/X recent search
- Reddit via PRAW
- Telegram Bot API
- Optional Google Trends via `pytrends`

### News

- GDELT
- NewsAPI
- Event Registry
- MediaStack
- Optional FAOSTAT enrichment

### Environmental

- OpenWeather
- NASA EarthData
- NOAA Climate Data Online
- Global Flood Monitoring System
- Copernicus Climate Data

### Alerting

- ReliefWeb API enrichment/submission pattern
- Slack webhook
- Discord webhook
- AWS SES
- Generic NGO webhook

## Crisis Scoring

Implemented in [backend/scoring/crisis_score.py](/Users/malcolmdyer/Documents/Hackathon Projects/backend/scoring/crisis_score.py).

```python
crisis_score = (
    0.4 * environmental_signals
    + 0.3 * news_signals
    + 0.2 * social_signals
    + 0.1 * historical_similarity
)
```

Thresholds:

- `0.0 - 0.3`: Normal
- `0.3 - 0.6`: Emerging Risk
- `0.6 - 0.8`: High Alert
- `0.8 - 1.0`: Crisis Likely

## Project Structure

```text
backend/
  alerts/
  data_sources/
  processing/
  scoring/
frontend/
  components/
main.py
requirements.txt
README.md
```

## How To Run

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Leave `DEMO_MODE=true` for the hackathon demo. Add API keys later for live ingestion.

### 3. Start the app

```bash
python3 main.py
```

Open `http://127.0.0.1:5000`.

## CLI Shortcuts

Run one monitoring pass:

```bash
python3 main.py --run-once
```

Run the critical drought demo:

```bash
python3 main.py --demo
```

## Demo Scenario

The built-in demo simulates an emerging drought-driven humanitarian crisis in Northern Kenya using:

- environmental drought anomalies
- tweets about food shortages and dry wells
- Telegram field updates describing migration
- news reports about crop failure and hunger

Expected outcome:

- a structured crisis report
- a crisis score in the `High Alert` or `Crisis Likely` range
- triggered alert dispatch payloads
- dashboard markers and feed updates

## Nemotron Reasoning Layer

Implemented in [backend/processing/reasoning.py](/Users/malcolmdyer/Documents/Hackathon Projects/backend/processing/reasoning.py).

The system includes:

- prompt builders for key event extraction
- prompt builders for crisis indicator assessment
- cross-source synthesis prompts
- a local deterministic fallback when no Nemotron endpoint is configured

This means the prototype is runnable without an LLM dependency, but ready to plug into a Nemotron-compatible inference endpoint later.

## Alert Payload Examples

Slack:

```json
{
  "text": "[High Alert] Northern Kenya crisis score=0.79"
}
```

Discord:

```json
{
  "content": "Global Crisis Signal Agent: Northern Kenya moved to High Alert"
}
```

NGO webhook:

```json
{
  "region": "Northern Kenya",
  "alert_level": "High Alert",
  "crisis_score": 0.79
}
```

## Notes

- The public ReliefWeb API is best used here as an enrichment channel and partner submission pattern, not a guaranteed anonymous publishing endpoint.
- Set `ENABLE_RELIEFWEB_LOOKUP=true` if you want the app to perform live ReliefWeb enrichment requests.
- GFMS and Copernicus are wired as pluggable HTTP adapters because production deployments usually depend on org-specific access patterns.
- The dashboard is static HTML/JS for speed and portability, with no frontend build step required.
