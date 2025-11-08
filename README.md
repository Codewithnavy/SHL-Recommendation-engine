# SHL Assessment Recommendation System

An intelligent recommendation system that helps hiring managers and recruiters find the most relevant SHL assessments for their job requirements using advanced natural language processing and semantic search.

## Problem Statement

Hiring managers often struggle to find the right assessments for their roles due to reliance on keyword searches and filters. This system uses AI to recommend the most relevant assessments from SHL's catalog based on natural language queries or job descriptions.

## Features

- Natural language query processing
- Semantic search using Google Gemini embeddings
- Balanced recommendations across test types (Knowledge & Skills, Personality & Behavior, etc.)
- REST API with health check and recommendation endpoints
- Web interface for easy testing
- Evaluation metrics including Mean Recall@K

## Technology Stack

- **Backend**: FastAPI (Python)
- **LLM**: Google Gemini API
- **Vector Database**: ChromaDB for semantic search
- **Web Scraping**: BeautifulSoup4 + Selenium
- **Data Processing**: Pandas, NumPy
- **Deployment**: Render / Railway (free tier)

## Project Structure

```
SHL_Assignment/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── recommender.py          # Recommendation engine
│   └── config.py               # Configuration
├── scraper/
│   └── shl_scraper.py          # Web scraper for SHL catalog
├── data/
│   ├── assessments.json        # Scraped assessment data
│   ├── train_set.csv           # Training data
│   └── test_set.csv            # Test queries
├── static/
│   └── index.html              # Frontend UI
├── evaluation/
│   ├── evaluate.py             # Evaluation metrics
│   └── generate_predictions.py # Generate test predictions
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

For detailed setup instructions, see [SETUP.md](SETUP.md).

### Quick Installation

```bash
git clone https://github.com/Codewithnavy/SHL-Recommendation-engine.git
cd SHL-Recommendation-engine
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
python verify_system.py  # Verify everything works
python app/main.py
```

Visit `http://localhost:8000` to access the web interface.

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (free tier available)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Codewithnavy/SHL-Recommendation-engine.git
cd SHL-Recommendation-engine
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

5. Scrape SHL assessment data:
```bash
python scraper/shl_scraper.py
```

6. Start the API server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Get Recommendations
```
POST /recommend
Request: {"query": "your job description or query"}
Response: {
  "recommended_assessments": [
    {
      "url": "assessment_url",
      "name": "assessment_name",
      "adaptive_support": "Yes/No",
      "description": "description",
      "duration": 60,
      "remote_support": "Yes/No",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```

## Usage Example

```python
import requests

response = requests.post(
    "http://localhost:8000/recommend",
    json={"query": "I am hiring for Java developers who can collaborate with business teams"}
)
print(response.json())
```

## Evaluation

The system is evaluated using Mean Recall@K metric:
- Measures how many relevant assessments are retrieved in top K recommendations
- Averaged across all test queries

Run evaluation:
```bash
python evaluation/evaluate.py
```

## Deployment

The application can be deployed to various platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Links:**
- GitHub Repository: https://github.com/Codewithnavy/SHL-Recommendation-engine
- API Documentation: Available at `/docs` endpoint when running
- Live Demo: Deploy using the instructions in DEPLOYMENT.md

## Approach Document

See [APPROACH.md](APPROACH.md) for detailed methodology and optimization strategies.

## Testing

Run the automated API tests:

```bash
# Start the server first
python app/main.py

# In another terminal
python test_api.py
```

## Additional Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide for various platforms
- [APPROACH.md](APPROACH.md) - Technical approach and methodology

## License

MIT License

## Author

Navneet Singh
