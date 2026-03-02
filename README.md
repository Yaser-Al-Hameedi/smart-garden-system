# Smart Garden System
AI-powered automated garden watering system running on Raspberry Pi 3B+.

## Setup

### 1. Clone the repo
```bash
git clone <repo-url>
cd smart-garden-system
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in your API key and GPS coordinates
```

### 5. Run locally (development)
```bash
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```
API docs available at: `http://localhost:8000/docs`

---

## Deploy to Raspberry Pi

### Prerequisites
- Pi is on the same network as your Mac
- SSH is enabled on the Pi
- You know the Pi's IP address

### Deploy
```bash
chmod +x deploy.sh
./deploy.sh <pi-ip-address>
```

### After deploying
Copy your `.env` file to the Pi manually (never commit secrets):
```bash
scp .env pi@<pi-ip-address>:/home/pi/smart-garden-system/.env
```

### Manage the service
```bash
# Check status
ssh pi@<pi-ip> "sudo systemctl status smart-garden"

# View logs
ssh pi@<pi-ip> "sudo journalctl -u smart-garden -f"

# Restart
ssh pi@<pi-ip> "sudo systemctl restart smart-garden"
```

---

## Project Structure
```
src/
├── main.py          # Entry point
├── sensors/         # Sensor reading (real + mock)
├── weather/         # OpenWeatherMap API client
├── pump/            # Relay/pump control
├── models/          # ML model integration
├── database/        # SQLite manager
├── api/             # FastAPI endpoints
└── scheduler/       # APScheduler jobs
tests/               # Test scripts
config/              # Settings
data/                # SQLite database (gitignored)
trained_models/      # ML model files (gitignored)
```
