#!/usr/bin/env python3
"""Test reset() and step() functionality"""

import requests
import json

BASE_URL = "https://devendranp-agentic-ai-app.hf.space"

print("=" * 60)
print("TESTING RESET AND STEP ENDPOINTS")
print("=" * 60)

# Test 1: Test /reset/easy endpoint
print("\n[1] Testing /reset/easy endpoint...")
try:
    response = requests.get(f"{BASE_URL}/reset/easy", timeout=10)
    print(f"    Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"    ✅ Response: {json.dumps(data, indent=6)}")
    else:
        print(f"    ❌ Error: {response.text}")
except Exception as e:
    print(f"    ❌ Exception: {e}")

# Test 2: Test /reset/medium endpoint
print("\n[2] Testing /reset/medium endpoint...")
try:
    response = requests.get(f"{BASE_URL}/reset/medium", timeout=10)
    print(f"    Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"    ✅ Response: {json.dumps(data, indent=6)}")
    else:
        print(f"    ❌ Error: {response.text}")
except Exception as e:
    print(f"    ❌ Exception: {e}")

# Test 3: Test /reset/hard endpoint
print("\n[3] Testing /reset/hard endpoint...")
try:
    response = requests.get(f"{BASE_URL}/reset/hard", timeout=10)
    print(f"    Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"    ✅ Response: {json.dumps(data, indent=6)}")
    else:
        print(f"    ❌ Error: {response.text}")
except Exception as e:
    print(f"    ❌ Exception: {e}")

# Test 4: Test /validate endpoint (contains step() test)
print("\n[4] Testing /validate endpoint (tests step() internally)...")
try:
    response = requests.get(f"{BASE_URL}/validate", timeout=10)
    print(f"    Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"    ✅ Validation Status: {data.get('openenv_compliance')}")
        print(f"    ✅ Steps completed:")
        for step in data.get('steps', []):
            print(f"       {step}")
    else:
        print(f"    ❌ Error: {response.text}")
except Exception as e:
    print(f"    ❌ Exception: {e}")

# Test 5: Test locally (no HF Space)
print("\n[5] Testing locally (direct environment import)...")
try:
    from src.env import EmergencyResponseEnv
    
    print("    Testing reset()...")
    env = EmergencyResponseEnv(task_difficulty="easy")
    state = env.reset()
    print(f"    ✅ reset() returned state with keys: {list(state.keys())}")
    
    print("    Testing step()...")
    action = {
        "ambulance_id": 1,
        "emergency_id": 1,
        "hospital_id": 1
    }
    next_state, reward, done, info = env.step(action)
    print(f"    ✅ step() returned: reward={reward}, done={done}")
    print(f"    ✅ next_state keys: {list(next_state.keys())}")
    
except Exception as e:
    print(f"    ❌ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
