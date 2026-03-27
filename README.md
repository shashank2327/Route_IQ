# RouteIQ 🗺️

An intelligent, AI-powered route planning system for field sales representatives. RouteIQ uses a two-agent pipeline built on **Google ADK** to automatically prioritize client visits and generate a traffic-aware optimized daily route — saving reps 2–3 hours of manual planning every day.

---

## Problem Statement

Field sales reps spend two to three hours every day choosing which clients to visit and in what order, relying on intuition rather than data. Managers lack real-time visibility into client clustering, traffic, and visit history. This leads to ineffective routes, unprepared client visits, and lost high-value opportunities.

## Solution

RouteIQ automates daily planning with a sequential two-agent pipeline:

1. **Agent 1 — Visit Prioritizer**: Scores and ranks every client in the CRM by deal stage urgency, days since last visit, and deal value. Selects the optimal number of clients for the day and generates deal-stage-specific talking points for each.
2. **Agent 2 — Route Builder**: Geocodes all selected client addresses via Google Maps, fetches real-time traffic-aware travel times, computes a nearest-neighbour optimized stop order, and attaches precise arrival/departure ETAs.

The rep pastes their CRM JSON into the **ADK Web Chat** interface and receives a fully formatted daily briefing streamed back live.

---

## Features

- 🎯 **Smart Client Prioritization** — Weighted scoring across deal stage (closing → prospecting), recency of last visit, and deal value
- 💬 **AI-Generated Talking Points** — 2–3 deal-stage-specific talking points per client so reps walk in prepared
- 🚦 **Live Traffic-Aware Route Optimization** — Real-time driving distances via Google Maps distance matrix + nearest-neighbour optimization
- ⏱️ **Precise ETA Scheduling** — 30-min visit buffer + actual drive time, with auto-drop of stops that exceed work hours
- 🌐 **ADK Web Chat Interface** — Fully browser-based; paste CRM JSON, get a markdown daily briefing streamed in real time

---

## Tech Stack

| Technology | Role |
|---|---|
| [Google ADK](https://google.github.io/adk-docs/) | Core multi-agent framework (`LlmAgent`, `SequentialAgent`), served via `adk web` |
| Google Gemini 2.5 Flash | LLM powering both agents for CRM reasoning, prioritization, and tool calling |
| Google Maps MCP Server | Provides `maps_geocode`, `maps_distance_matrix`, and `maps_directions` for real-time routing |
| Model Context Protocol (MCP) | Seamless integration between the route builder agent and the Maps API |
| Python 3.11+ | Backend language with `google-adk`, `python-dotenv`, and `pydantic` |
| Node.js / npx | Used to run the Google Maps MCP server (`@modelcontextprotocol/server-google-maps`) |

---

## Project Structure

```
RouteIQ/
├── route_iq_agent/
│   ├── agent.py              # Root agent entry point & input sanitizer callback
│   ├── pipeline/
│   │   └── sequential.py     # Wires the two agents into a SequentialAgent pipeline
│   ├── agents/
│   │   ├── prioritizer.py    # Agent 1 — Visit Prioritizer (pure LLM reasoning)
│   │   └── route_builder.py  # Agent 2 — Route Builder (uses Google Maps MCP)
│   ├── tools/
│   │   └── maps_mcp.py       # Google Maps MCPToolset factory
│   └── prompts/
│       ├── prioritizer.txt   # System prompt for Agent 1
│       └── route_builder.txt # System prompt for Agent 2
├── input.json                # Example CRM input payload
├── requirements.txt          # Python dependencies
└── .env                      # API keys (not committed)
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for the Maps MCP server)
- A **Google Gemini API key**
- A **Google Maps API key** (with Maps JavaScript API, Geocoding API, Distance Matrix API, and Directions API enabled)

### 1. Clone the repository

```bash
git clone https://github.com/shashank2327/Route_IQ.git
cd Route_IQ
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
GOOGLE_GENAI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### 5. Run the ADK web interface

```bash
adk web
```

Open [http://localhost:8000](http://localhost:8000) in your browser and select the `route_iq_agent`.

---

## Usage

Paste your CRM data as JSON into the chat. Use `input.json` as a reference:

```json
{
  "rep": {
    "rep_name": "Priya Sharma",
    "start_location": "91 Springboard, Koramangala, Bengaluru, Karnataka 560034",
    "start_time": "09:00",
    "max_visits": 2,
    "work_hours": "09:00-18:00"
  },
  "clients": [
    {
      "client_name": "Biocon Limited",
      "address": "Biocon Park, Jigani Link Rd, Bommasandra, Bengaluru, Karnataka 560099",
      "last_visit_date": "2026-02-20",
      "deal_stage": "closing",
      "deal_value_usd": 200000
    }
  ]
}
```

The pipeline will stream back a formatted daily briefing with prioritized clients, talking points, an optimized route, and arrival/departure ETAs for each stop.

---

## How the Pipeline Works

```
User pastes CRM JSON
       │
       ▼
 [Input Sanitizer]  ← before_agent_callback strips raw JSON into
       │               plain text to prevent ADK template conflicts
       ▼
 [Agent 1: Visit Prioritizer]
   • Scores clients by deal stage, recency, deal value
   • Selects top N clients for the day
   • Generates talking points per client
       │
       │  (output passed as context to Agent 2)
       ▼
 [Agent 2: Route Builder]
   • Geocodes each address (maps_geocode)
   • Fetches traffic-aware travel times (maps_distance_matrix)
   • Optimizes stop order (nearest-neighbour)
   • Attaches ETAs (30 min visit + drive time)
   • Drops stops exceeding work hours
   • Fetches full directions (maps_directions)
       │
       ▼
 Formatted Markdown Daily Briefing streamed to browser
```

---

## License

This project is licensed under the MIT License.
