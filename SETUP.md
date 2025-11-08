# SHL Assessment Recommendation System - Setup Guide

## Quick Start

Follow these steps to set up and run the application locally.

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- Google Gemini API key (free tier available)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Codewithnavy/SHL-Recommendation-engine.git
cd SHL-Recommendation-engine
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

**Get a free API key:**
- Visit: https://ai.google.dev/gemini-api/docs/pricing
- Sign in with Google account
- Generate API key (free tier: 60 requests/minute)

### Step 5: Initialize Assessment Data

The project includes a pre-populated assessment database. If you want to refresh it:

```bash
python scraper/shl_scraper.py
```

This will scrape the latest data from the SHL catalog (or use the fallback dataset).

### Step 6: Run the Application

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python app/main.py
```

The API will be available at: `http://localhost:8000`

### Step 7: Test the Application

**Option 1: Web Interface**
- Open your browser and navigate to: `http://localhost:8000`
- Use the web interface to test queries

**Option 2: API Testing**

Test health endpoint:
```bash
curl http://localhost:8000/health
```

Test recommendation endpoint:
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"I am hiring for Java developers who can collaborate with business teams\"}"
```

**Option 3: Python Script**
```python
import requests

response = requests.post(
    "http://localhost:8000/recommend",
    json={"query": "I need a Senior Data Analyst with SQL and Python skills"}
)
print(response.json())
```

## Running Evaluation

To evaluate the system on the training set:

```bash
python evaluation/evaluate.py
```

This will:
- Load training data
- Generate recommendations for each query
- Calculate Mean Recall@K
- Save results to `evaluation/train_evaluation_results.json`

## Generating Test Predictions

To generate predictions for the test set:

```bash
python evaluation/generate_predictions.py
```

This will:
- Load test queries
- Generate recommendations
- Save results to `predictions.csv` in the required format

## Project Structure Explained

```
SHL_Assignment/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic data models
│   ├── recommender.py       # Core recommendation engine
│   └── config.py            # Configuration settings
├── scraper/
│   ├── __init__.py
│   └── shl_scraper.py       # Web scraper for SHL catalog
├── data/
│   ├── assessments.json     # Assessment database
│   ├── train_set.csv        # Training data with labels
│   └── test_set.csv         # Test queries
├── static/
│   └── index.html           # Frontend web interface
├── evaluation/
│   ├── __init__.py
│   ├── evaluate.py          # Evaluation metrics
│   └── generate_predictions.py  # Test set prediction generator
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── APPROACH.md             # Technical approach document
└── SETUP.md                # This file
```

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
pip install google-generativeai
```

### Issue: "API key not found"

**Solution:**
- Ensure `.env` file exists in the project root
- Check that `GOOGLE_API_KEY` is set correctly
- Restart the server after updating `.env`

### Issue: "No assessments found"

**Solution:**
- Check that `data/assessments.json` exists
- Run the scraper: `python scraper/shl_scraper.py`
- The fallback data will be created automatically

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use a different port
python -m uvicorn app.main:app --port 8001
```

## Development Mode

For development with auto-reload:

```bash
uvicorn app.main:app --reload --log-level debug
```

## Production Deployment

See README.md for deployment instructions to Render or Railway.

## Testing

Manual testing checklist:
- [ ] Health endpoint responds
- [ ] Recommendation endpoint accepts queries
- [ ] Returns 5-10 recommendations
- [ ] Response format matches specification
- [ ] Web interface loads correctly
- [ ] Example queries work
- [ ] Error handling for invalid queries

## Getting Help

If you encounter issues:
1. Check this setup guide
2. Review the error logs
3. Ensure all dependencies are installed
4. Verify API key is valid
5. Check the GitHub repository for updates

## Next Steps

After setup:
1. Explore the web interface
2. Test with custom queries
3. Review the approach document (APPROACH.md)
4. Run evaluation to see performance metrics
5. Generate predictions for test set
6. Deploy to production (optional)
