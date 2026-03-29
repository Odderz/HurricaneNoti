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
