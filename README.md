# Global Crisis Signal Agent

AI-powered humanitarian crisis early warning system built during the NVIDIA Hackathon at San José State University.

The platform ingests social, news, and environmental data streams, detects emerging anomalies, computes weighted crisis likelihood scores, and dispatches alerts through a live dashboard.

---

## My Role

I co-developed this project during the NVIDIA Hackathon.

My contributions included:

- Implementing backend data ingestion and processing workflows
- Supporting anomaly detection, AI-assisted reasoning, and crisis scoring workflows
- Rapidly implementing backend and application features during hackathon development
- Connecting APIs, processing pipelines, and dashboard outputs
- Assisting with system integration and live demo preparation
- Collaborating under rapid hackathon development timelines

---

## NVIDIA Hackathon Context

This project was developed during the NVIDIA Hackathon at San José State University as a rapid AI-assisted prototype focused on humanitarian crisis detection workflows.

The hackathon emphasized:
- rapid prototyping
- practical AI integration
- accelerated development workflows
- experimentation with NVIDIA Nemotron-style reasoning systems

The platform was designed to demonstrate how AI-assisted signal synthesis and anomaly detection could support earlier humanitarian crisis awareness and response coordination.

---

## Problem

Humanitarian crises often become visible to institutions only after multiple warning signs have already converged:

- drought signals
- migration chatter
- food market stress
- regional news coverage
- local social reporting

Analysts lose valuable response time when those signals remain fragmented across APIs, dashboards, and reporting systems.

---

## Solution

Global Crisis Signal Agent normalizes multi-source signals into a unified processing pipeline that:

1. Collects real-time crisis indicators
2. Cleans and normalizes incoming data
3. Detects anomalies and geographic clustering
4. Applies AI-assisted reasoning workflows
5. Computes weighted crisis likelihood scores
6. Dispatches alerts and updates a live dashboard

The prototype supports both:
- demo simulation mode
- live API ingestion mode

---

# System Architecture

```text
APIs -> Source Clients -> Unified Signal Schema -> Cleaning Pipeline
    -> Indicator Extraction -> Historical Similarity -> AI Reasoning Layer
    -> Crisis Score Engine -> Alert Dispatcher -> Flask API -> Dashboard
```

---

## Core Processing Flow

1. Collect real-time social, news, and environmental signals
2. Clean and deduplicate signal streams
3. Detect spikes, clustering, and multi-source confirmation
4. Run structured AI-assisted reasoning workflows
5. Compute weighted crisis severity scores
6. Trigger alerts and update the monitoring dashboard

---

# APIs & Data Sources

## Social Sources

- Twitter/X Recent Search
- Reddit via PRAW
- Telegram Bot API
- Google Trends (optional)

## News Sources

- GDELT
- NewsAPI
- Event Registry
- MediaStack

## Environmental Sources

- OpenWeather
- NASA EarthData
- NOAA Climate Data
- Global Flood Monitoring System
- Copernicus Climate Data

---

# Crisis Scoring Engine

```python
crisis_score = (
    0.4 * environmental_signals
    + 0.3 * news_signals
    + 0.2 * social_signals
    + 0.1 * historical_similarity
)
```

## Risk Thresholds

| Score Range | Alert Level |
|---|---|
| 0.0 - 0.3 | Normal |
| 0.3 - 0.6 | Emerging Risk |
| 0.6 - 0.8 | High Alert |
| 0.8 - 1.0 | Crisis Likely |

---

# Technologies Used

## Backend

- Python
- Flask
- REST APIs

## AI & Data Processing

- NVIDIA Nemotron-style reasoning workflows
- Anomaly detection
- Signal normalization
- Historical similarity analysis

## Infrastructure & Integration

- Slack webhooks
- Discord webhooks
- AWS SES
- NGO alert webhooks

---

# Project Structure

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

---

# Demo Scenario

The built-in demo simulates an emerging drought-driven humanitarian crisis in Northern Kenya using:

- environmental drought anomalies
- food shortage reports
- migration-related Telegram updates
- regional crop failure news reports

Expected outcomes include:

- structured crisis reports
- weighted crisis likelihood scores
- triggered alert dispatch payloads
- live dashboard updates

---

# AI Reasoning Layer

The platform includes AI-assisted reasoning workflows for:

- key event extraction
- crisis indicator assessment
- cross-source synthesis
- severity evaluation

The system supports deterministic local fallback logic when no external AI inference endpoint is configured.

---

# Alert Integrations

Supported integrations include:

- Slack
- Discord
- AWS SES
- NGO webhooks
- ReliefWeb enrichment patterns

---

# How To Run

## 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure Environment

```bash
cp .env.example .env
```

Leave:

```text
DEMO_MODE=true
```

enabled for the demo scenario.

---

## 3. Start the Application

```bash
python3 main.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Demo Commands

Run one monitoring cycle:

```bash
python3 main.py --run-once
```

Run the Northern Kenya demo scenario:

```bash
python3 main.py --demo
```

---

# Screenshots

(Add dashboard screenshots here)

---

# Future Improvements

- Real-time streaming ingestion
- Distributed processing workers
- Enhanced AI threat reasoning
- Geospatial visualization
- Advanced anomaly detection
- Multi-region monitoring support

---

# NVIDIA Hackathon Project

Built during the NVIDIA Hackathon at San José State University as a rapid prototype focused on AI-assisted humanitarian crisis detection and response workflows.
