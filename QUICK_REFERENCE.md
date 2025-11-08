# Quick Reference - SHL Assessment Recommendation System

## Essential Commands

### Setup (One-time)
```bash
cd c:\Users\navne\SHL_Assignment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```

### Run Application
```bash
cd c:\Users\navne\SHL_Assignment
venv\Scripts\activate
python app/main.py
```
Access at: http://localhost:8000

### Test API
```bash
# In a new terminal
cd c:\Users\navne\SHL_Assignment
venv\Scripts\activate
python test_api.py
```

### Run Evaluation
```bash
cd c:\Users\navne\SHL_Assignment
venv\Scripts\activate
python evaluation/evaluate.py
```

### Generate Predictions
```bash
cd c:\Users\navne\SHL_Assignment
venv\Scripts\activate
python evaluation/generate_predictions.py
```
Output: predictions.csv

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```
Response: `{"status": "healthy"}`

### Get Recommendations
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"I need Java developers who can collaborate\"}"
```

## File Locations

- **API Code:** `app/main.py`, `app/recommender.py`
- **Frontend:** `static/index.html`
- **Data:** `data/assessments.json`
- **Tests:** `test_api.py`, `evaluation/`
- **Docs:** `README.md`, `APPROACH.md`, `SETUP.md`

## Key Features

1. Semantic search with Gemini embeddings
2. Balanced recommendations (technical + behavioral)
3. 5-10 assessments per query
4. Web interface + REST API
5. Evaluation framework included

## Deployment

See DEPLOYMENT.md for full guide.

**Quick Deploy to Render:**
1. Go to https://render.com
2. New Web Service → Connect GitHub
3. Set GOOGLE_API_KEY environment variable
4. Deploy!

## Common Issues

**Issue:** Module not found
**Fix:** `pip install -r requirements.txt`

**Issue:** API key error
**Fix:** Check `.env` file has GOOGLE_API_KEY set

**Issue:** Port already in use
**Fix:** Change port: `uvicorn app.main:app --port 8001`

## Submission Checklist

- [ ] Deploy application (get URL)
- [ ] Run: `python evaluation/generate_predictions.py`
- [ ] Collect: API URL, GitHub URL, predictions.csv
- [ ] Verify all endpoints work
- [ ] Submit!

## Links

- GitHub: https://github.com/Codewithnavy/SHL-Recommendation-engine
- Docs: http://localhost:8000/docs (when running)
- Web UI: http://localhost:8000 (when running)
