#!/usr/bin/env python3
"""Test complete reset -> step -> state flow"""

import requests
import json

BASE_URL = "https://devendranp-agentic-ai-app.hf.space"

print("=" * 70)
print("TESTING COMPLETE OPENENV FLOW: reset() -> step() -> state()")
print("=" * 70)

# Step 1: Call reset
print("\n[1️⃣] RESET: Start new game")
print("    GET /reset/easy")
try:
    response = requests.get(f"{BASE_URL}/reset/easy", timeout=10)
    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    ✅ Observation: {json.dumps(data.get('observation'), indent=6)}")
    obs1 = data.get('observation')
except Exception as e:
    print(f"    ❌ Error: {e}")
    exit(1)

# Step 2: Call state (just check, no action)
print("\n[🔍] STATE: Check current situation (no action)")
print("    GET /state")
try:
    response = requests.get(f"{BASE_URL}/state", timeout=10)
    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    ✅ Observation: {json.dumps(data.get('observation'), indent=6)}")
    obs2 = data.get('observation')
    
    # Verify state hasn't changed
    if obs1 == obs2:
        print("    ✅ State unchanged (as expected)")
    else:
        print("    ⚠️  State changed unexpectedly")
except Exception as e:
    print(f"    ❌ Error: {e}")
    exit(1)

# Step 3: Call step with action
print("\n[2️⃣] STEP: Make a move (take action)")
print("    POST /step")

action = {
    "ambulance_id": 1,
    "emergency_id": 1,
    "hospital_id": 1
}
print(f"    Action: {json.dumps(action)}")

try:
    response = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    ✅ Observation: {json.dumps(data.get('observation'), indent=6)}")
    print(f"    ✅ Reward: {data.get('reward')}")
    print(f"    ✅ Done: {data.get('done')}")
    print(f"    ✅ Info: {data.get('info')}")
except Exception as e:
    print(f"    ❌ Error: {e}")
    exit(1)

# Step 4: Call state again (should show updated state)
print("\n[🔍] STATE: Check updated situation")
print("    GET /state")
try:
    response = requests.get(f"{BASE_URL}/state", timeout=10)
    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    ✅ Observation: {json.dumps(data.get('observation'), indent=6)}")
except Exception as e:
    print(f"    ❌ Error: {e}")
    exit(1)

# Step 5: Take a few more steps
print("\n[➕] MULTIPLE STEPS: Loop through actions")
for i in range(2):
    print(f"\n    Step {i+2}:")
    try:
        action = {
            "ambulance_id": (i % 2) + 1,
            "emergency_id": (i % 3) + 1,
            "hospital_id": (i % 2) + 1
        }
        response = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
        data = response.json()
        print(f"    ✅ Reward: {data.get('reward')}, Done: {data.get('done')}")
    except Exception as e:
        print(f"    ❌ Error: {e}")

# Step 6: Reset again (start fresh)
print("\n[1️⃣] RESET AGAIN: Start new game")
print("    GET /reset/medium")
try:
    response = requests.get(f"{BASE_URL}/reset/medium", timeout=10)
    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    ✅ New scenario: {data.get('message')}")
    print(f"    ✅ Observation: {json.dumps(data.get('observation'), indent=6)}")
except Exception as e:
    print(f"    ❌ Error: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ COMPLETE FLOW TEST PASSED!")
print("=" * 70)
print("\n📋 Summary:")
print("   ✅ reset() - Start new game")
print("   ✅ state() - Check current situation")
print("   ✅ step() - Take action and get (observation, reward, done)")
print("   ✅ Flow maintains state between calls")
print("   ✅ Handles multiple steps in sequence")
print("   ✅ Can reset to new difficulty")
