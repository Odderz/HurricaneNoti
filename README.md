# 🌀 HurricaneNoti

A multi-agent AI system that tracks hurricanes in real-time and helps US residents stay safe.

## Features
- 🌀 Live NOAA hurricane tracking
- 📍 Zip code based danger assessment
- 🗺️ Interactive emergency resource map (hospitals, shelters, fire stations, police)
- 📧 Real-time email alerts
- 🔄 Self-healing fallback when live APIs fail

## Built With
- Google ADK (Agent Development Kit)
- Groq LLaMA 3.3 70B
- NOAA National Hurricane Center API
- OpenStreetMap / Folium
- Gmail SMTP

## Challenges
- Google Cloud ADK Challenge
- Climate Teach-In Tampa Bay Resilience Challenge

## How It Works
1. User enters their zip code
2. StormTracker agent checks NOAA for active hurricanes
3. Safety agent assesses danger level for their location
4. Resource map is generated with nearby emergency locations
5. Email alert sent to user with safety instructions

## Agents
- **StormTrackerAgent** — monitors live NOAA National Hurricane Center data
- **LocationAgent** — resolves zip codes to coordinates
- **SafetyAgent** — assesses danger level and generates emergency resource map
- **ParallelObserverAgent** — designed to run StormTracker and Location simultaneously

## Self-Healing
When live data APIs fail, HurricaneNoti automatically falls back to verified Tampa Bay emergency resource data — ensuring users always receive critical safety information even during network outages.

## Demo
1. Clone the repo
2. Add your API keys to `.env`
3. Run `adk web`
4. Open `http://localhost:8000`
