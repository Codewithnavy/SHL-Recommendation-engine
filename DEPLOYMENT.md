# Deployment Guide - SHL Assessment Recommendation System

This guide covers deploying the application to free cloud platforms.

## Option 1: Deploy to Render (Recommended)

Render offers a generous free tier perfect for this application.

### Prerequisites
- GitHub account with the repository
- Google Gemini API key

### Steps

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up using your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Codewithnavy/SHL-Recommendation-engine`
   - Click "Connect"

3. **Configure Service**
   - Name: `shl-recommendation-api` (or your choice)
   - Region: Choose closest to your location
   - Branch: `main`
   - Root Directory: Leave empty
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Key: `GOOGLE_API_KEY`
   - Value: Your Gemini API key
   - Click "Add"

5. **Deploy**
   - Instance Type: Select "Free"
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

6. **Access Your Application**
   - Once deployed, you'll get a URL like: `https://shl-recommendation-api.onrender.com`
   - Test the health endpoint: `https://your-app.onrender.com/health`
   - Access the web interface: `https://your-app.onrender.com`

### Important Notes for Render

- Free tier may spin down after inactivity (takes 30-60s to wake up)
- Build time: ~3-5 minutes
- First request after sleep: ~30 seconds
- Subsequent requests: Fast

## Option 2: Deploy to Railway

Railway is another excellent free option.

### Steps

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `SHL-Recommendation-engine`

3. **Configure Environment**
   - Click on the service
   - Go to "Variables" tab
   - Add: `GOOGLE_API_KEY` = your API key
   - Add: `PORT` = 8000

4. **Configure Start Command**
   - Go to "Settings" tab
   - Under "Start Command", enter:
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

5. **Deploy**
   - Railway will automatically deploy
   - Check the deployment logs
   - Once complete, click "Generate Domain"

6. **Access Application**
   - Use the generated domain like: `https://your-app.up.railway.app`

## Option 3: Deploy to Heroku

### Steps

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd SHL_Assignment
   heroku create shl-recommendation-system
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_api_key_here
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open Application**
   ```bash
   heroku open
   ```

## Option 4: Deploy to Google Cloud Run

For more advanced deployments with better performance.

### Steps

1. **Install Google Cloud SDK**
   - Download from https://cloud.google.com/sdk

2. **Create Dockerfile**
   Already included in project.

3. **Deploy**
   ```bash
   gcloud run deploy shl-recommendation \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your_key
   ```

## Environment Variables Required

All platforms need these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| GOOGLE_API_KEY | Gemini API key | AIza... |
| PORT | Server port (auto-set by most platforms) | 8000 |

## Post-Deployment Checklist

After deployment, verify:

- [ ] Health endpoint responds: `GET /health`
- [ ] Returns `{"status": "healthy"}`
- [ ] Recommendation endpoint works: `POST /recommend`
- [ ] Web interface loads correctly
- [ ] HTTPS is enabled
- [ ] CORS is configured for your domain

## Testing Your Deployed API

### Using cURL

```bash
# Test health
curl https://your-app-url.com/health

# Test recommendation
curl -X POST https://your-app-url.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "I need a Java developer assessment"}'
```

### Using Python

```python
import requests

BASE_URL = "https://your-app-url.com"

# Health check
health = requests.get(f"{BASE_URL}/health")
print(health.json())

# Get recommendations
response = requests.post(
    f"{BASE_URL}/recommend",
    json={"query": "Senior Data Analyst with SQL and Python"}
)
print(response.json())
```

### Using JavaScript/Browser

```javascript
// Test in browser console
fetch('https://your-app-url.com/recommend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    query: 'Java developer with collaboration skills'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

## Monitoring and Logs

### Render
- Dashboard → Your Service → Logs
- Real-time log streaming
- Error tracking

### Railway
- Project → Service → Deployments → View Logs
- Metrics dashboard available

### Heroku
```bash
heroku logs --tail
```

## Performance Optimization

### For Free Tier

1. **Keep App Awake**
   - Use UptimeRobot or similar to ping every 25 minutes
   - Prevents cold starts

2. **Optimize Cold Starts**
   - Assessment data is pre-loaded in repo
   - Embeddings are cached after first use
   - Lightweight dependencies

3. **Monitor Usage**
   - Gemini free tier: 60 requests/minute
   - Cache embeddings to reduce API calls
   - Implement rate limiting if needed

## Troubleshooting

### Issue: "Application Error" or 500 errors

**Check:**
- Environment variables are set correctly
- Build logs for errors
- Runtime logs for exceptions

**Solution:**
```bash
# View logs and check for missing dependencies
# Ensure GOOGLE_API_KEY is set
# Verify PORT variable is available
```

### Issue: Cold starts taking too long

**Solution:**
- Normal for free tier (30-60s)
- Consider using UptimeRobot to keep alive
- Or upgrade to paid tier

### Issue: "Module not found" errors

**Solution:**
- Ensure `requirements.txt` is complete
- Check build logs
- Verify Python version compatibility

## Updating Your Deployment

### Render/Railway (Auto-deploy)
- Push to GitHub main branch
- Platforms will auto-deploy

### Heroku (Manual)
```bash
git push heroku main
```

### Force Redeploy
- Most platforms have "Manual Deploy" button
- Use this if auto-deploy isn't triggered

## Security Considerations

1. **Never commit API keys** to GitHub
2. **Use environment variables** for secrets
3. **Enable HTTPS** (automatic on most platforms)
4. **Monitor usage** to prevent abuse
5. **Set rate limits** if needed

## Cost Considerations

### Free Tier Limits

**Render:**
- 750 hours/month (enough for 1 app 24/7)
- Spins down after 15 min inactivity
- No credit card required

**Railway:**
- $5 free credit/month
- No credit card required initially
- ~140 hours of runtime

**Heroku:**
- 1000 dyno hours/month (with credit card verification)
- Sleeps after 30 min inactivity

## Support

If you encounter deployment issues:

1. Check platform status pages
2. Review deployment logs
3. Verify environment variables
4. Test locally first
5. Check GitHub repository issues

## Next Steps After Deployment

1. Add deployment URL to your README
2. Test all endpoints thoroughly
3. Submit the deployment URL for evaluation
4. Monitor logs for any issues
5. Consider adding analytics

---

**Recommended Platform:** Render (easiest setup, most reliable free tier)

**Deployment Time:** 5-10 minutes

**Maintenance:** Minimal (auto-deploys from GitHub)
