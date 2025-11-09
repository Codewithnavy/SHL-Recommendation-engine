"""
Keep-alive script to prevent Render free tier from sleeping.
This script pings the health endpoint every 10 minutes.
"""

import requests
import time
import os
from datetime import datetime

# Your Render deployment URL
RENDER_URL = os.getenv("RENDER_URL", "https://shl-recommendation-engine-l6f9.onrender.com")
PING_INTERVAL = 600  # 10 minutes in seconds

def ping_service():
    """Ping the health endpoint to keep service awake."""
    try:
        response = requests.get(f"{RENDER_URL}/health", timeout=30)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if response.status_code == 200:
            print(f"[{timestamp}] ✓ Service is alive - Status: {response.status_code}")
            return True
        else:
            print(f"[{timestamp}] ⚠ Service responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✗ Failed to ping service: {str(e)}")
        return False

def main():
    """Main keep-alive loop."""
    print(f"Starting keep-alive service for: {RENDER_URL}")
    print(f"Ping interval: {PING_INTERVAL} seconds ({PING_INTERVAL//60} minutes)")
    print("-" * 60)
    
    while True:
        ping_service()
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()
