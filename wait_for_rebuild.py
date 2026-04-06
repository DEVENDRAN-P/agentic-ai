#!/usr/bin/env python3
"""Wait for Space rebuild and test endpoints"""

import time
import requests

BASE_URL = "https://devendranp-agentic-ai-app.hf.space"

print("Waiting 120 seconds for HF Space to fully rebuild...")
for i in range(12):
    try:
        r = requests.get(f"{BASE_URL}/state", timeout=5)
        if r.status_code == 200:
            print(f"✅ /state endpoint is now available! (after {i*10}s)")
            break
    except:
        pass
    if i < 11:
        time.sleep(10)
        print(f"  {i+1}/12 - Still waiting...")

print()
print("Testing endpoints:")

try:
    # Reset
    r = requests.get(f"{BASE_URL}/reset/easy", timeout=10)
    print(f"GET /reset/easy: {r.status_code}")
    data = r.json()
    obs_key = "observation" if "observation" in data else "state"
    print(f'  Returns "{obs_key}" key: {obs_key in data}')
except Exception as e:
    print(f"  Error: {e}")

try:
    # State
    r = requests.get(f"{BASE_URL}/state", timeout=10)
    print(f"GET /state: {r.status_code}")
except Exception as e:
    print(f"GET /state: Error - {e}")

try:
    # Step
    r = requests.post(f"{BASE_URL}/step", json={"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}, timeout=10)
    print(f"POST /step: {r.status_code}")
except Exception as e:
    print(f"POST /step: Error - {e}")

print()
print("✅ If all show 200 - endpoints are ready!")
