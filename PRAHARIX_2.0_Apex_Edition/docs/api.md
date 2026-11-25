# PRAHARIX 3.0 — API Reference

## Base URL
`http://localhost:5000`

## Authentication
All admin endpoints require session cookie with `role=admin`.

## Core Endpoints

### Status
`GET /api/status` — Platform health check

### Weather
`GET /api/weather` — Live weather data (Mumbai HQ)

### Earthquakes
`GET /api/earthquakes` — Live seismic events (USGS + NCS)

## AI Endpoints

### AI Summary
`GET /api/ai/summary` — Trilingual situational summary

### AI Query
`GET /api/ai/query?query=<text>` — Natural language query processor

### What-If Simulation
`GET /api/ai/whatif?hazard=flood&rainfall=200&district=Kolhapur`

## V3 Disaster Intelligence Endpoints

### Explainable Risk
`GET /api/v3/risk/explain?district=Kolhapur`

### Multi-Hazard Score
`GET /api/v3/risk/multihazard?district=Kolhapur&rainfall=200`

### District Heatmap
`GET /api/v3/risk/heatmap`

### Flood Area Estimation
`GET /api/v3/flood/area?district=Kolhapur&rainfall=250`

### Earthquake Impact
`GET /api/v3/earthquake/impact?district=Kolhapur&mag=6.2&depth=10`

### Cyclone Impact
`GET /api/v3/cyclone/impact?district=Ratnagiri&wind=130&rainfall=200`

### Smart Evacuation Routes
`GET /api/v3/evacuation/routes?district=Kolhapur&hazard=flood`

### Ambulance Allocation
`GET /api/v3/response/ambulances?district=Kolhapur&severity=HIGH&casualties=50`

### Rescue Team Allocation
`GET /api/v3/response/rescue-teams?district=Kolhapur&severity=HIGH&hazard=FLOOD`

### Response Priorities
`GET /api/v3/response/priorities`

### Response Progress
`GET /api/v3/response/progress?incident_id=INC-MH-2026-001`

## Performance Endpoints

`GET /api/v3/performance/metrics` — Response time stats
`GET /api/v3/db/optimize` — Database optimization report
`GET /api/v3/load/simulate?users=50` — Load test simulation
`GET /api/v3/simulation/historical?year=2019` — Historical disaster replay
`GET /api/v3/analytics/model-accuracy` — Precision/recall analysis
`GET /api/v3/cache/stats` — Cache statistics
