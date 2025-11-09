# API Endpoint Documentation

## Base URL
```
http://localhost:8000
```
(When deployed, replace with your Render/Railway URL)

---

## 1. Health Check Endpoint

**Endpoint:** `GET /health`

**Description:** Check if the API is running

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 2. Get Recommendations Endpoint (Main API)

**Endpoint:** `POST /recommend`

**Description:** Get assessment recommendations based on a job description or query

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "query": "your job description or query text here"
}
```

### PowerShell Examples:

**Example 1: Basic Query**
```powershell
$body = '{"query":"Java developer with 3 years experience"}'
Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -Body $body -ContentType "application/json"
```

**Example 2: Detailed Job Description**
```powershell
$body = @"
{
  "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment that can be completed in 40 minutes."
}
"@
Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -Body $body -ContentType "application/json"
```

**Example 3: Format Response as JSON**
```powershell
$body = '{"query":"Python Data Analyst with SQL skills"}'
$response = Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

### Response Format:

```json
{
  "query": "your original query",
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/solutions/products/...",
      "name": "Core Java (Advanced)",
      "adaptive_support": "Yes",
      "description": "Assessment description here...",
      "duration": 40,
      "remote_support": "Yes",
      "test_type": ["Technical", "Coding"]
    },
    {
      "url": "https://www.shl.com/solutions/products/...",
      "name": "Another Assessment",
      "adaptive_support": "No",
      "description": "Another description...",
      "duration": 30,
      "remote_support": "Yes",
      "test_type": ["Behavioral"]
    }
    // ... 5-10 assessments total
  ]
}
```

### Response Fields:

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | The original query you sent |
| `recommended_assessments` | array | List of 5-10 recommended assessments |
| `url` | string | Link to the assessment on SHL website |
| `name` | string | Assessment name |
| `adaptive_support` | string | "Yes" or "No" - whether assessment is adaptive |
| `description` | string | Full description of the assessment |
| `duration` | integer | Time in minutes |
| `remote_support` | string | "Yes" or "No" - whether remote testing supported |
| `test_type` | array | List of test categories (e.g., "Technical", "Behavioral") |

---

## 3. API Documentation UI

**Endpoint:** `GET /docs`

**Description:** Interactive Swagger UI for testing the API

**URL:** http://localhost:8000/docs

Open this in your browser to:
- See all endpoints
- Test them interactively
- View request/response schemas

---

## cURL Examples (Alternative to PowerShell)

If you have cURL installed:

```bash
# Health check
curl http://localhost:8000/health

# Get recommendations
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"query":"Java developer with Spring Boot experience"}'
```

---

## Python Example

```python
import requests

url = "http://localhost:8000/recommend"
payload = {
    "query": "Senior Data Analyst with SQL and Python expertise"
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Query: {data['query']}")
print(f"Found {len(data['recommended_assessments'])} recommendations:")

for i, assessment in enumerate(data['recommended_assessments'], 1):
    print(f"\n{i}. {assessment['name']}")
    print(f"   Duration: {assessment['duration']} minutes")
    print(f"   URL: {assessment['url']}")
```

---

## JavaScript/Fetch Example

```javascript
const query = "QA Engineer with automation testing skills";

fetch('http://localhost:8000/recommend', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: query })
})
.then(response => response.json())
.then(data => {
    console.log('Recommendations:', data.recommended_assessments);
})
.catch(error => console.error('Error:', error));
```

---

## Error Responses

**400 Bad Request** - Invalid query (too short or missing)
```json
{
  "detail": "Query must be at least 10 characters"
}
```

**500 Internal Server Error** - Server issue
```json
{
  "detail": "Error message here"
}
```

---

## Rate Limits

- **Development (localhost):** No limits
- **Production (deployed):** Depends on your hosting plan
- **Google Gemini API:** 60 requests/minute (if API key configured)

---

## Quick Test

**Step 1:** Make sure server is running
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Step 2:** Test in new PowerShell window
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Get recommendations
$body = '{"query":"Java developer"}'
Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -Body $body -ContentType "application/json"
```

**Step 3:** View in browser
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Production URL (After Deployment)

Once deployed to Render/Railway, replace `http://localhost:8000` with your production URL:

```
https://your-app-name.onrender.com/recommend
```

Example:
```powershell
$body = '{"query":"Python developer"}'
Invoke-RestMethod -Uri "https://shl-recommendation-engine.onrender.com/recommend" -Method Post -Body $body -ContentType "application/json"
```

---

## Summary

✅ **Main Endpoint:** `POST /recommend`  
✅ **Input:** JSON with `query` field  
✅ **Output:** JSON with 5-10 recommended assessments  
✅ **Test UI:** http://localhost:8000  
✅ **API Docs:** http://localhost:8000/docs  

Your API is ready to use! 🚀
