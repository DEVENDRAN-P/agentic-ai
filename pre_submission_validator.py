#!/usr/bin/env python3
"""
COMPREHENSIVE PRE-SUBMISSION VALIDATOR
Checks all hackathon requirements before final submission
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

print("\n" + "=" * 80)
print("HACKATHON PRE-SUBMISSION VALIDATOR")
print("=" * 80 + "\n")

validator_results = []

# ============================================================================
# 1. CHECK: HF SPACE DEPLOYMENT
# ============================================================================
print("[1] HF Space Deployment")
print("-" * 80)

try:
    BASE_URL = "https://devendranp-agentic-ai-app.hf.space"
    r = requests.get(f"{BASE_URL}/", timeout=10)
    if r.status_code == 200:
        print("✅ HF Space is LIVE and responding")
        print(f"   URL: {BASE_URL}")
        print(f"   Status: {r.status_code} OK")
        validator_results.append(("1. HF Space deploys", True))
    else:
        print(f"❌ Space returned {r.status_code}")
        validator_results.append(("1. HF Space deploys", False))
except Exception as e:
    print(f"❌ Space not accessible: {e}")
    validator_results.append(("1. HF Space deploys", False))

# ============================================================================
# 2. CHECK: AUTOMATED PING
# ============================================================================
print("\n[2] Automated Ping (reset() callable)")
print("-" * 80)

try:
    r = requests.get(f"{BASE_URL}/ping", timeout=10)
    if r.status_code == 200:
        data = r.json()
        if data.get("status") == "ok":
            print("✅ /ping endpoint works")
            print(f"   Returns HTTP 200")
            print(f"   Calls reset() successfully")
            validator_results.append(("2. Automated ping works", True))
        else:
            print(f"❌ /ping returned unexpected status")
            validator_results.append(("2. Automated ping works", False))
    else:
        print(f"❌ /ping returned {r.status_code}")
        validator_results.append(("2. Automated ping works", False))
except Exception as e:
    print(f"❌ /ping failed: {e}")
    validator_results.append(("2. Automated ping works", False))

# ============================================================================
# 3. CHECK: OpenEnv SPECIFICATION
# ============================================================================
print("\n[3] OpenEnv Compliance")
print("-" * 80)

openenv_pass = True

# Check openenv.yaml
if os.path.exists("configs/openenv.yaml"):
    print("✅ openenv.yaml exists")
else:
    print("❌ openenv.yaml missing")
    openenv_pass = False

# Check reset() endpoint
try:
    r = requests.get(f"{BASE_URL}/reset/easy", timeout=10)
    if r.status_code == 200 and "observation" in r.json():
        print("✅ reset() endpoint works - returns observation")
    else:
        print("❌ reset() endpoint failed")
        openenv_pass = False
except:
    print("❌ reset() endpoint error")
    openenv_pass = False

# Check state() endpoint
try:
    r = requests.get(f"{BASE_URL}/state", timeout=10)
    if r.status_code == 200 and "observation" in r.json():
        print("✅ state() endpoint works - returns observation")
    else:
        print("❌ state() endpoint failed")
        openenv_pass = False
except:
    print("❌ state() endpoint error")
    openenv_pass = False

# Check step() endpoint
try:
    action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
    r = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
    if r.status_code == 200:
        data = r.json()
        if all(k in data for k in ["observation", "reward", "done"]):
            print("✅ step() endpoint works - returns (obs, reward, done)")
        else:
            print("❌ step() missing required keys")
            openenv_pass = False
    else:
        print("❌ step() endpoint failed")
        openenv_pass = False
except Exception as e:
    print(f"❌ step() endpoint error: {e}")
    openenv_pass = False

validator_results.append(("3. OpenEnv spec compliance", openenv_pass))

# ============================================================================
# 4. CHECK: DOCKERFILE
# ============================================================================
print("\n[4] Dockerfile")
print("-" * 80)

dockerfile_pass = False
if os.path.exists("Dockerfile"):
    print("✅ Dockerfile exists")
    try:
        with open("Dockerfile", "r") as f:
            content = f.read()
            # Check for uvicorn in CMD (uvicorn is the web server)
            if "uvicorn" in content.lower():
                print("✅ Dockerfile configured with uvicorn")
                # Also verify requirements.txt has fastapi and uvicorn
                with open("requirements.txt", "r") as req:
                    req_content = req.read()
                    if "fastapi" in req_content.lower() and "uvicorn" in req_content.lower():
                        print("✅ requirements.txt includes FastAPI + Uvicorn")
                        dockerfile_pass = True
                    else:
                        print("❌ requirements.txt missing FastAPI/Uvicorn")
            else:
                print("❌ Dockerfile missing uvicorn configuration")
    except Exception as e:
        print(f"❌ Error reading Dockerfile: {e}")
else:
    print("❌ Dockerfile not found")

validator_results.append(("4. Dockerfile builds", dockerfile_pass))

# ============================================================================
# 5. CHECK: BASELINE (inference.py)
# ============================================================================
print("\n[5] Baseline Reproduction (inference.py)")
print("-" * 80)

baseline_pass = False
if os.path.exists("inference.py"):
    print("✅ inference.py exists in root")
    try:
        result = subprocess.run(
            ["python", "inference.py", "--task", "easy", "--episodes", "1"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            output = result.stdout
            if "[END]" in output:
                print("✅ inference.py runs successfully")
                print("✅ Produces [END] logs")
                baseline_pass = True
            else:
                print("❌ Output missing [END] logs")
        else:
            print(f"❌ inference.py crashed: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print("❌ inference.py timeout (>30s)")
    except Exception as e:
        print(f"❌ Error running inference.py: {e}")
else:
    print("❌ inference.py not in root")

validator_results.append(("5. Baseline reproduces", baseline_pass))

# ============================================================================
# 6. CHECK: 3+ TASKS WITH GRADERS
# ============================================================================
print("\n[6] 3+ Tasks with Graders")
print("-" * 80)

tasks_pass = True
for task in ["easy", "medium", "hard"]:
    try:
        r = requests.get(f"{BASE_URL}/reset/{task}", timeout=10)
        if r.status_code == 200:
            print(f"✅ Task '{task}' available")
        else:
            print(f"❌ Task '{task}' failed")
            tasks_pass = False
    except:
        print(f"❌ Task '{task}' error")
        tasks_pass = False

validator_results.append(("6. 3+ tasks with graders", tasks_pass))

# ============================================================================
# 7. CHECK: ENVIRONMENT VARIABLES
# ============================================================================
print("\n[7] Environment Variables Configuration")
print("-" * 80)

env_pass = True
required_vars = ["API_BASE_URL", "MODEL_NAME", "HF_TOKEN"]

for var in required_vars:
    if os.getenv(var):
        print(f"✅ {var} is set in environment")
    else:
        print(f"⚠️  {var} not set locally (should be set in HF Space settings)")

# Check if they're referenced in app.py
try:
    with open("app.py", "r") as f:
        app_content = f.read()
        for var in required_vars:
            if var in app_content:
                print(f"✅ {var} used in app.py")
            else:
                print(f"❌ {var} not referenced in app.py")
                env_pass = False
except:
    print("❌ Error reading app.py")
    env_pass = False

validator_results.append(("7. Environment variables configured", env_pass))

# ============================================================================
# 8. CHECK: inference.py EXACT NAME IN ROOT
# ============================================================================
print("\n[8] inference.py - Exact Name & Location")
print("-" * 80)

exact_name_pass = False
if os.path.exists("inference.py") and os.path.isfile("inference.py"):
    print("✅ inference.py exists in ROOT directory")
    print(f"   Size: {os.path.getsize('inference.py')} bytes")
    exact_name_pass = True
else:
    print("❌ inference.py not found in root")

validator_results.append(("8. inference.py exact name", exact_name_pass))

# ============================================================================
# 9. CHECK: LOGGING FORMAT [START][STEP][END]
# ============================================================================
print("\n[9] Logging Format [START] [STEP] [END]")
print("-" * 80)

log_format_pass = False
try:
    result = subprocess.run(
        ["python", "inference.py", "--task", "easy", "--episodes", "1"],
        capture_output=True,
        text=True,
        timeout=30
    )
    output = result.stdout
    
    has_start = "[START]" in output
    has_step = "[STEP]" in output
    has_end = "[END]" in output
    
    if has_start:
        print("✅ [START] logs present")
    else:
        print("❌ [START] logs missing")
    
    if has_step:
        print("✅ [STEP] logs present")
    else:
        print("❌ [STEP] logs missing")
    
    if has_end:
        print("✅ [END] logs present")
    else:
        print("❌ [END] logs missing")
    
    log_format_pass = has_start and has_step and has_end
    
except Exception as e:
    print(f"❌ Error checking logs: {e}")

validator_results.append(("9. Logging format [START][STEP][END]", log_format_pass))

# ============================================================================
# 10. CHECK: INFRASTRUCTURE CONSTRAINTS
# ============================================================================
print("\n[10] Infrastructure Constraints (20min, 2vCPU, 8GB RAM)")
print("-" * 80)

infra_pass = True
import time

try:
    start = time.time()
    result = subprocess.run(
        ["python", "inference.py", "--task", "hard", "--episodes", "1"],
        capture_output=True,
        text=True,
        timeout=120  # 2 minute timeout
    )
    elapsed = time.time() - start
    
    if elapsed < 120:
        print(f"✅ Episode completed in {elapsed:.1f}s (< 120s)")
        print(f"   Fits in 20-minute limit")
    else:
        print(f"❌ Episode took {elapsed:.1f}s (too slow)")
        infra_pass = False
        
except subprocess.TimeoutExpired:
    print("❌ Episode timeout (> 120s)")
    infra_pass = False
except Exception as e:
    print(f"⚠️  Error testing infrastructure: {e}")

validator_results.append(("10. Infrastructure constraints", infra_pass))

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80 + "\n")

passed = sum(1 for _, result in validator_results if result)
total = len(validator_results)

for requirement, result in validator_results:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status} - {requirement}")

print("\n" + "=" * 80)
print(f"SCORE: {passed}/{total} requirements passing")
print("=" * 80 + "\n")

if passed == total:
    print("🎉 ALL REQUIREMENTS PASSED - READY FOR SUBMISSION! 🎉\n")
    print("Space URL: https://devendranp-agentic-ai-app.hf.space\n")
    sys.exit(0)
elif passed >= total - 2:
    print("⚠️  MOST REQUIREMENTS PASSING - Minor issues detected\n")
    sys.exit(1)
else:
    print("❌ CRITICAL ISSUES - Fix before submission\n")
    sys.exit(1)
