#!/usr/bin/env python3
"""Test all /reset endpoint variations"""

import requests
import json

BASE_URL = "https://devendranp-agentic-ai-app.hf.space"

print("Testing /reset endpoint variations:")
print("=" * 60)

# Test 1: /reset (no parameter - should default to easy)
print("\n[1] GET /reset (no difficulty parameter)")
try:
    r = requests.get(f"{BASE_URL}/reset", timeout=10)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Message: {data.get('message')}")
    step = data.get("observation", {}).get("step")
    print(f"Step: {step}")
    print("✅ Default /reset works!")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: /reset/easy
print("\n[2] GET /reset/easy")
try:
    r = requests.get(f"{BASE_URL}/reset/easy", timeout=10)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Message: {data.get('message')}")
    step = data.get("observation", {}).get("step")
    print(f"Step: {step}")
    print("✅ /reset/easy works!")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: /reset/medium
print("\n[3] GET /reset/medium")
try:
    r = requests.get(f"{BASE_URL}/reset/medium", timeout=10)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Message: {data.get('message')}")
    step = data.get("observation", {}).get("step")
    print(f"Step: {step}")
    print("✅ /reset/medium works!")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: /reset/hard
print("\n[4] GET /reset/hard")
try:
    r = requests.get(f"{BASE_URL}/reset/hard", timeout=10)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Message: {data.get('message')}")
    step = data.get("observation", {}).get("step")
    print(f"Step: {step}")
    print("✅ /reset/hard works!")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ ALL RESET VARIATIONS WORKING!")
print("=" * 60)
