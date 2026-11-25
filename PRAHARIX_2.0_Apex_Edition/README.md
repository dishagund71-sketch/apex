# 🚨 PRAHARIX 2.0 — Apex Edition

<div align="center">

**National & Global Multi-Hazard Disaster Command Platform**

*Production-grade AI-powered disaster intelligence, early warning, and response coordination system built for India's national defense and disaster management ecosystem.*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</div>

---

## 🎯 Overview

**PRAHARIX 2.0 Apex Edition** is a full-stack Flask-based disaster command intelligence platform integrating:

- 🛰️ **Live Satellite Telemetry** — real-time satellite data feeds and Copernicus SAR imagery
- 🌊 **Multi-Hazard Engine** — earthquakes, floods, cyclones, tsunamis, industrial hazards, wildfires
- ⚡ **Seismic Early Warning (EEW)** — Earthquake Early Warning with NDMA CAP protocol alerts
- 🤖 **AI Decision Trees** — intelligent triage, resource dispatch, and SITREP generation
- 🗺️ **IMD Doppler Radar Integration** — live cyclone tracking with IMD radar stations
- 🪂 **NDRF Battalion Dispatch Matrix** — optimal force allocation across seismic zones
- 🌐 **Global Command View** — international disaster monitoring and coordination
- 📡 **SAR (Search & Rescue) Module** — Copernicus SAR product integration
- 📊 **Natural Language Query Processing** — conversational situational awareness
- 🏛️ **Government Operations Portal** — administrative command interface

---

## 🏗️ Architecture

```
PRAHARIX_2.0_Apex_Edition/
│
├── app.py                  # 🧠 Core Flask Engine — routes, auth, API hub
├── apex_engine.py          # ⚙️ Apex AI decision & prediction engine
├── disaster_intel.py       # 🌪️ Disaster intelligence & data processing
├── hazard_engine.py        # ⚡ Multi-hazard cascade simulation engine
├── india_tactical.py       # 🇮🇳 India-specific: EEW, NDRF, IMD, seismic zones
├── live_apis.py            # 🌐 Live external API integrations (USGS, IMD, etc.)
├── govt_ops.py             # 🏛️ Government operations & admin portal backend
├── sar_module.py           # 🪂 Search & Rescue + Copernicus SAR integration
├── manage.py               # 🔧 App management utilities
│
├── templates/              # 🖥️ Jinja2 HTML templates
│   ├── index.html          # Main dashboard
│   ├── apex.html           # Apex command view
│   ├── predict.html        # AI prediction interface
│   ├── multihazard.html    # Multi-hazard simulation
│   ├── global.html         # Global disaster monitoring
│   ├── india.html          # India-specific command view
│   ├── govt.html           # Government operations portal
│   ├── alerts.html         # Real-time alert management
│   ├── sar.html            # Search & Rescue module
│   ├── analytics.html      # Analytics dashboard
│   └── ...
│
├── static/                 # 📦 Static assets (audio, images, CSS/JS)
├── requirements.txt        # 📋 Python dependencies
├── .env.example            # 🔐 Environment variable template
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites

- Python **3.11+**
- `pip` or `conda`
- (Optional) `virtualenv` or `venv`

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PRAHARIX_2.0_Apex_Edition.git
cd PRAHARIX_2.0_Apex_Edition
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the template
copy .env.example .env       # Windows
cp .env.example .env         # Linux/macOS

# Edit .env with your actual values
# Generate a secure SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

### 6. Production Deployment (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## ⚙️ Key Modules

| Module | Purpose |
|---|---|
| `app.py` | Flask core: routing, auth, session management, API orchestration |
| `apex_engine.py` | AI-driven triage, prediction, and autonomous SITREP generation |
| `disaster_intel.py` | Disaster data ingestion, classification, and intelligence fusion |
| `hazard_engine.py` | Multi-hazard cascade modeling (earthquake → tsunami → flood chains) |
| `india_tactical.py` | EEW lead time calculation, NDRF dispatch matrix, IMD radar integration |
| `live_apis.py` | Live feeds: USGS, IMD, GDACS, Copernicus, NDMA CAP |
| `govt_ops.py` | Government operations command interface backend |
| `sar_module.py` | Copernicus SAR product pipeline + risk scoring for SAR missions |

---

## 🔐 Environment Variables

See [`.env.example`](.env.example) for all configuration options.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask cryptographic session key (generate with `secrets.token_hex(32)`) |
| `ADMIN_USERNAME` | Admin portal username |
| `ADMIN_PASSWORD` | Admin portal password (plain text, hashed at runtime) |
| `USER_USERNAME` | Standard user username |
| `USER_PASSWORD` | Standard user password |
| `SESSION_COOKIE_SECURE` | Set `True` for HTTPS production |
| `FLASK_DEBUG` | Set `False` in production |
| `FLASK_HOST` | Server bind address (default: `127.0.0.1`) |
| `FLASK_PORT` | Server port (default: `5000`) |

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

---

## 🧪 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask 3.1 |
| **AI / ML** | scikit-learn, PyTorch, ultralytics (YOLO) |
| **Geospatial** | GeoPandas, Rasterio, Folium, PyProj, Shapely |
| **Data** | Pandas, NumPy, Polars |
| **Satellite** | sentinelhub, OpenCV |
| **Reports** | ReportLab (PDF generation) |
| **Deployment** | Gunicorn, Uvicorn |
| **Frontend** | Jinja2, HTML5, CSS3, JavaScript |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact

Built for national disaster management and emergency response operations.

> *"Speed of response saves lives."*
