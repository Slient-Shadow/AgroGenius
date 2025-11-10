
# AGROGENIUS — Seed Quality Analyzer

## Setup
1. Place your trained model `unet_model.h5` in the project root.
2. (Optional) replace `static/logo.png` and `static/sample_seed.png` with your assets.

### Run locally (development)
```bash
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8080
```

Open http://localhost:8080

### Build & Run with Docker
```bash
docker build -t agrogenius .
docker run -p 8080:8080 -e PORT=8080 agrogenius
```

### Deploy to Cloud Run (Google Cloud)
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/agrogenius
gcloud run deploy agrogenius --image gcr.io/YOUR_PROJECT_ID/agrogenius --platform managed --region asia-south1 --allow-unauthenticated
```

After deploy, you'll get a public URL.
