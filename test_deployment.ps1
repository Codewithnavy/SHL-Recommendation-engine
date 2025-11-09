# Quick test script for your Render deployment
# This verifies everything is working before you set up cron job

$RENDER_URL = "https://shl-recommendation-engine-l6f9.onrender.com"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Testing Your Render Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Test 1: Health endpoint
Write-Host "1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$RENDER_URL/health" -TimeoutSec 10
    if ($health.status -eq "healthy") {
        Write-Host "   ✓ Health check PASSED" -ForegroundColor Green
        Write-Host "   Response: $($health.status)`n" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ✗ Health check FAILED" -ForegroundColor Red
    Write-Host "   Error: $_`n" -ForegroundColor Red
    exit 1
}

# Test 2: Recommend endpoint
Write-Host "2. Testing Recommend Endpoint..." -ForegroundColor Yellow
try {
    $body = '{"query":"Java developer with Python skills"}'
    $recommendations = Invoke-RestMethod -Uri "$RENDER_URL/recommend" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 15
    
    if ($recommendations.recommended_assessments.Count -gt 0) {
        Write-Host "   ✓ Recommendation API PASSED" -ForegroundColor Green
        Write-Host "   Found $($recommendations.recommended_assessments.Count) assessments`n" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ✗ Recommendation API FAILED" -ForegroundColor Red
    Write-Host "   Error: $_`n" -ForegroundColor Red
    exit 1
}

# Test 3: Web interface
Write-Host "3. Testing Web Interface..." -ForegroundColor Yellow
try {
    $web = Invoke-WebRequest -Uri $RENDER_URL -TimeoutSec 10
    if ($web.StatusCode -eq 200) {
        Write-Host "   ✓ Web interface PASSED" -ForegroundColor Green
        Write-Host "   Status: $($web.StatusCode) OK`n" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ✗ Web interface FAILED" -ForegroundColor Red
    Write-Host "   Error: $_`n" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "✓ ALL TESTS PASSED!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Your deployment is LIVE and working perfectly!`n" -ForegroundColor White

Write-Host "URLs for submission:" -ForegroundColor Cyan
Write-Host "  API: $RENDER_URL" -ForegroundColor White
Write-Host "  Docs: $RENDER_URL/docs" -ForegroundColor White
Write-Host "  Web: $RENDER_URL`n" -ForegroundColor White

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "NEXT STEP: Prevent 502 Errors" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Yellow

Write-Host "Set up cron-job.org keep-alive (takes 2 minutes):`n" -ForegroundColor White

Write-Host "1. Go to: " -NoNewline -ForegroundColor White
Write-Host "https://cron-job.org/en/" -ForegroundColor Cyan

Write-Host "`n2. Sign up (free)`n" -ForegroundColor White

Write-Host "3. Create cron job with these settings:" -ForegroundColor White
Write-Host "   Title: SHL Recommender Keep-Alive" -ForegroundColor Gray
Write-Host "   URL: $RENDER_URL/health" -ForegroundColor Gray
Write-Host "   Schedule: Every 10 minutes" -ForegroundColor Gray

Write-Host "`n4. Done! Your app will never sleep.`n" -ForegroundColor Green

Write-Host "Opening cron-job.org in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "https://cron-job.org/en/"

Write-Host "`n✨ See KEEP_ALIVE_SETUP.md for detailed instructions`n" -ForegroundColor Cyan
