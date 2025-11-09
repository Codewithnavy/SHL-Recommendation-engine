# API Key Setup Guide

## Current Status

✅ **System is working with keyword-based recommendations**
⚠️ **Google Gemini API key not configured (optional for better accuracy)**

## Two Operating Modes

### 1. Keyword-Based Mode (Current - No API Key Needed)
- ✅ Works immediately without setup
- ✅ Fast and reliable
- ✅ Good accuracy for clear technical terms
- ✅ Free forever
- ⚠️ Less sophisticated semantic understanding

### 2. Semantic Search Mode (Requires Free API Key)
- ✅ Better semantic understanding
- ✅ Understands context and meaning
- ✅ More accurate for complex queries
- ✅ Still free (60 requests/minute)
- ⚠️ Requires 5-minute setup

## How to Enable Semantic Search (Optional)

### Step 1: Get Your Free API Key (2 minutes)

1. Visit: **https://ai.google.dev/gemini-api/docs/api-key**

2. Click the blue **"Get an API key"** button

3. Sign in with your Google account (Gmail, etc.)

4. Choose one of:
   - **"Create API key in new project"** (recommended)
   - Or select an existing Google Cloud project

5. Copy the generated API key (starts with "AIza...")
   - It looks like: `AIzaSyB...` (37 characters)

### Step 2: Add Key to .env File (1 minute)

**Option A: Use the setup script**
```bash
python setup_api_key.py
```
This will open the .env file for you automatically.

**Option B: Manual setup**

1. Open the file: `c:\Users\navne\SHL_Assignment\.env`

2. Find the line:
   ```
   GOOGLE_API_KEY=
   ```

3. Add your key after the equals sign:
   ```
   GOOGLE_API_KEY=AIzaSyB...your_actual_key_here
   ```

4. Save the file

### Step 3: Verify (30 seconds)

Run the verification:
```bash
python verify_system.py
```

You should see:
```
✓ Gemini API configured successfully
```

### Step 4: Test It

Run the application:
```bash
python app/main.py
```

Or generate predictions:
```bash
python evaluation/generate_predictions.py
```

## Troubleshooting

### "GOOGLE_API_KEY not set"
- Make sure you saved the .env file
- Check there are no spaces around the equals sign
- Restart your terminal/command prompt

### "Could not configure Gemini API"
- Verify your API key is correct (starts with AIza)
- Check you copied the entire key (37 characters)
- Make sure there are no quotes around the key in .env

### "API quota exceeded"
- Free tier: 60 requests/minute, 1,500/day
- Wait a minute and try again
- System will automatically fall back to keyword mode

## Free Tier Limits

✅ **60 requests per minute** - More than enough
✅ **1,500 requests per day** - Plenty for development
✅ **No credit card required**
✅ **No time limit**

## Do I Really Need This?

**NO!** The system works great without it:
- ✅ Predictions.csv was generated successfully
- ✅ 90 recommendations across 9 queries
- ✅ Good relevance matching
- ✅ All features working

**Benefits of adding API key:**
- Better understanding of natural language
- More nuanced matching
- Slightly higher accuracy
- But keyword mode is already quite good!

## Quick Commands

**Check if API key is set:**
```bash
python setup_api_key.py
```

**Test without API key:**
```bash
python evaluation/generate_predictions.py
```
(This works and generates good results!)

**Test with API key:**
```bash
# After setting GOOGLE_API_KEY in .env
python evaluation/generate_predictions.py
```
(Even better results with semantic understanding!)

## Summary

- **Current Status**: ✅ System working, predictions generated
- **API Key**: Optional for enhanced accuracy
- **Setup Time**: 5 minutes total
- **Cost**: Free forever
- **Required for Submission**: NO - system works without it!

The choice is yours! Both modes work well.
