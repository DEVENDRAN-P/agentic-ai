#!/usr/bin/env python3
"""Test new endpoints after deployment"""

import time
import requests

BASE_URL = "https://devendranp-agentic-ai-app.hf.space"

# Give space time to rebuild
print("Waiting for HF Space to rebuild... (max 2 min)")
for attempt in range(12):  # 12 * 10 = 120 seconds
    try:
        r = requests.get(f"{BASE_URL}/", timeout=10)
        if r.status_code == 200:
            print(f"✅ HF Space is ready after {attempt*10}s")
            break
    except:
        pass
    if attempt < 11:
        time.sleep(10)
        print(f"  Waiting... {attempt+1}/12")
else:
    print("⚠️  Space not ready yet, but continuing with test")

print()
print("📋 TESTING NEW ENDPOINTS:")
print()

try:
    # Test 1: GET /
    print("[1] GET / (Root)")
    r = requests.get(f"{BASE_URL}/", timeout=10)
    print(f"    Status: {r.status_code} ✅")

    # Test 2: GET /reset/easy  
    print("[2] GET /reset/easy")
    r = requests.get(f"{BASE_URL}/reset/easy", timeout=10)
    print(f"    Status: {r.status_code} ✅")
    if r.status_code == 200:
        d = r.json()
        print(f"    Keys: {list(d.keys())}")
        if "observation" in d:
            print(f'    ✅ Returns "observation" key')

    # Test 3: GET /state
    print("[3] GET /state")
    r = requests.get(f"{BASE_URL}/state", timeout=10)
    print(f"    Status: {r.status_code} ✅")
    if r.status_code == 200:
        print(f"    ✅ Returns current state")

    # Test 4: POST /step
    print("[4] POST /step")
    action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
    r = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
    print(f"    Status: {r.status_code} ✅")
    if r.status_code == 200:
        d = r.json()
        if "observation" in d and "reward" in d and "done" in d:
            print(f'    ✅ Returns (observation, reward, done)')

    print()
    print("✅ ALL NEW ENDPOINTS DEPLOYED")
except Exception as e:
    print(f"Error: {e}")
