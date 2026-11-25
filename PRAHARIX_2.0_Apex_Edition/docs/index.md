# PRAHARIX 3.0 — Technical Documentation

## Overview
PRAHARIX (Predictive Risk Assessment Hub And Response Intelligence eXchange) 3.0 is a production-grade national disaster management and intelligence platform.

## Key Features
- **80 upgrade items** across 8 categories
- Real-time multi-hazard risk assessment
- Explainable AI risk scoring
- District-wise heatmaps for all 36 Maharashtra districts
- Emergency response automation
- WCAG 2.2 AA accessibility compliance
- Trilingual support (Hindi/Marathi/English)
- Offline PWA with service worker
- Complete test coverage

## Tech Stack
- **Backend:** Python 3.11 + Flask 3.1
- **Database:** SQLite (upgradeable to PostgreSQL)
- **AI/ML:** scikit-learn + Custom Physics Engines
- **GIS:** GeoPandas, Folium, Shapely
- **APIs:** USGS, OpenWeatherMap, NASA FIRMS, GDACS

## Quick Start
```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints
See [API Reference](api.md) for complete endpoint documentation.

## Running Tests
```bash
python -m pytest tests/ -v --cov=. --cov-report=html
```
