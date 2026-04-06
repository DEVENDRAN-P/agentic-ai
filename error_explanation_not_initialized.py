#!/usr/bin/env python3
"""
Explanation: Why "Environment not initialized. Call /reset first." Error Occurs
Shows the FastAPI endpoint workflow and initialization requirements
"""

import json

print("=" * 80)
print("❌ ERROR: \"Environment not initialized. Call /reset first.\"")
print("=" * 80)

print("\n🔍 WHAT CAUSES THIS ERROR?")
print("-" * 80)

explanation = """
This error occurs when you try to use the FastAPI endpoints WITHOUT first
initializing the environment.

In app.py (line 23), there's a global variable:
    _current_env: Optional[Any] = None

This means the environment starts as EMPTY (None).

When you call /step or /state endpoints, the code checks:
    if _current_env is None:
        raise ValueError("Environment not initialized. Call /reset first.")

If you skipped the /reset endpoint, the environment is still None, so you get
this error!
"""

print(explanation)

print("\n📊 THE API ENDPOINT WORKFLOW")
print("-" * 80)

workflow = {
    "1. START": {
        "status": "❌ Environment is None",
        "code": "_current_env = None",
        "action": "Nothing initialized yet"
    },
    "↓": {},
    "2. CALL /reset/{difficulty}": {
        "status": "✅ Environment created",
        "code": "_current_env = EmergencyResponseEnv(difficulty)",
        "action": "Initializes environment and returns initial state",
        "example": "GET /reset/easy"
    },
    "↓": {},
    "3. NOW YOU CAN CALL /step": {
        "status": "✅ Environment exists",
        "code": "_current_env.step(action)",
        "action": "Takes action and returns new state",
        "example": "POST /step with action"
    },
    "↓": {},
    "4. OR CALL /state": {
        "status": "✅ Environment exists",
        "code": "_current_env.state()",
        "action": "Returns current state",
        "example": "GET /state"
    }
}

for step, details in workflow.items():
    if step.startswith("↓"):
        print("    ⬇️")
        continue
    
    print(f"\n{step}")
    for key, value in details.items():
        print(f"  {key:15} {value}")

print("\n\n" + "=" * 80)
print("✅ HOW TO FIX THIS ERROR")
print("=" * 80)

print("\n📋 CORRECT API CALL SEQUENCE:")
print("-" * 80)

# Show in different formats
formats = {
    "cURL (Command Line)": """
# Step 1: Initialize environment
curl -X GET "http://localhost:7860/reset/easy"

# Step 2: Take an action
curl -X POST "http://localhost:7860/step" \\
  -H "Content-Type: application/json" \\
  -d '{"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}'

# Step 3: Get current state (optional)
curl -X GET "http://localhost:7860/state"
    """,
    
    "Python Requests": """
import requests

BASE_URL = "http://localhost:7860"

# Step 1: Initialize environment
response = requests.get(f"{BASE_URL}/reset/easy")
print("Environment reset:", response.json())

# Step 2: Take an action
action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
response = requests.post(f"{BASE_URL}/step", json=action)
print("Step result:", response.json())

# Step 3: Get current state
response = requests.get(f"{BASE_URL}/state")
print("Current state:", response.json())
    """,
    
    "JavaScript/Fetch": """
const BASE_URL = "http://localhost:7860";

// Step 1: Initialize environment
const resetResponse = await fetch(`${BASE_URL}/reset/easy`);
const resetData = await resetResponse.json();
console.log("Environment reset:", resetData);

// Step 2: Take an action
const action = {ambulance_id: 1, emergency_id: 1, hospital_id: 1};
const stepResponse = await fetch(`${BASE_URL}/step`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify(action)
});
const stepData = await stepResponse.json();
console.log("Step result:", stepData);

// Step 3: Get current state
const stateResponse = await fetch(`${BASE_URL}/state`);
const stateData = await stateResponse.json();
console.log("Current state:", stateData);
    """
}

for language, code in formats.items():
    print(f"\n{language}:")
    print(code)

print("\n" + "=" * 80)
print("⚡ QUICK START - START HERE")
print("=" * 80)

print("""
If you're using the CLI instead of the FastAPI endpoints:

    # Step 1: Run inference directly (no REST API needed)
    python inference.py --task easy --episodes 1 --agent heuristic
    
    # DONE! No need to call /reset manually.

If you're using FastAPI web interface:

    # Step 1: Start the server
    uvicorn app:app --reload --host 0.0.0.0 --port 7860
    
    # Step 2: Visit in browser or use curl/requests
    # FIRST:  http://localhost:7860/reset/easy
    # THEN:   POST to /step with action
    # FINALLY: GET /state to check current state
""")

print("\n" + "=" * 80)
print("📝 ENDPOINT REFERENCE")
print("=" * 80)

endpoints = {
    "GET /reset/{difficulty}": {
        "What it does": "Initialize environment with given difficulty",
        "Required first?": "✅ YES - MUST call this first!",
        "Parameters": "difficulty: 'easy', 'medium', or 'hard'",
        "Returns": "Initial observation/state",
        "Example": "GET /reset/easy"
    },
    
    "POST /step": {
        "What it does": "Execute one action in the environment",
        "Required first?": "❌ NO - Call /reset first!",
        "Parameters": "{'ambulance_id': int, 'emergency_id': int, 'hospital_id': int}",
        "Returns": "New observation, reward, done flag",
        "Example": "POST /step with body: {\"ambulance_id\": 1, \"emergency_id\": 1, \"hospital_id\": 1}"
    },
    
    "GET /state": {
        "What it does": "Get current state without taking action",
        "Required first?": "❌ NO - Call /reset first!",
        "Parameters": "None",
        "Returns": "Current observation/state",
        "Example": "GET /state"
    },
    
    "GET /ping": {
        "What it does": "Health check - creates temp environment",
        "Required first?": "✅ Can call anytime",
        "Parameters": "None",
        "Returns": "Health status",
        "Example": "GET /ping"
    }
}

for endpoint, info in endpoints.items():
    print(f"\n{endpoint}")
    for key, value in info.items():
        print(f"  {key:20} {value}")

print("\n" + "=" * 80)
print("🎯 SUMMARY")
print("=" * 80)

summary = """
ERROR: "Environment not initialized. Call /reset first."

CAUSE: You called /step or /state WITHOUT calling /reset first

SOLUTION: Always follow this order:
   1. Call GET /reset/{difficulty}   (initializes environment)
   2. Call POST /step                 (takes actions)
   3. Call GET /state                 (checks current state)

QUICK TEST:
   # In browser:
   http://localhost:7860/reset/easy
   
   # Then POST to /step with action in body
   
For CLI users: Just run inference.py - no manual initialization needed!
"""

print(summary)

print("=" * 80)
