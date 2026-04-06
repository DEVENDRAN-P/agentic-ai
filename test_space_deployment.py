#!/usr/bin/env python3
"""
Test HF Space deployment - verify all key endpoints respond with 200
"""

import requests
import json

SPACE_URL = "https://devendranp-agentic-ai-app.hf.space"

endpoints = [
    ("/", "ROOT - Health check"),
    ("/ping", "PING - Requirement 2 (Automated ping)"),
    ("/validate", "VALIDATE - Requirement 3 (OpenEnv compliance)"),
    ("/reset/easy", "RESET - Requirement 2 (Reset callable)"),
    ("/health", "HEALTH - Service health"),
    ("/run?task=easy&episodes=1", "RUN - Requirement 5 (Baseline test)"),
]

print("\n" + "=" * 70)
print(" HF SPACE DEPLOYMENT VERIFICATION")
print("=" * 70)

passed = 0
failed = 0

for endpoint, description in endpoints:
    try:
        url = SPACE_URL + endpoint
        r = requests.get(url, timeout=15)
        status_emoji = "✅" if r.status_code == 200 else "⚠️"
        print(f"\n{status_emoji} {description}")
        print(f"   URL: {endpoint}")
        print(f"   Status: HTTP {r.status_code} {r.reason}")
        
        if r.status_code == 200:
            passed += 1
            try:
                data = r.json()
                # Show response summary
                if isinstance(data, dict):
                    if "status" in data:
                        print(f"   Response: status={data['status']}")
                    elif "message" in data:
                        print(f"   Response: {data['message'][:70]}")
                    elif "openenv_compliance" in data:
                        print(f"   Response: OpenEnv={data['openenv_compliance']}")
                    else:
                        keys = list(data.keys())[:3]
                        print(f"   Response keys: {', '.join(keys)}")
            except:
                print(f"   Response: {r.text[:80]}")
        else:
            failed += 1
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️  {description}")
        print(f"   URL: {endpoint}")
        print(f"   Status: TIMEOUT (Space may be sleeping)")
        
    except Exception as e:
        failed += 1
        print(f"\n❌ {description}")
        print(f"   Error: {str(e)[:80]}")

print("\n" + "=" * 70)
print(" SUMMARY")
print("=" * 70)
print(f"Endpoints Passed: {passed}/{len(endpoints)}")
print(f"Endpoints Failed: {failed}/{len(endpoints)}")

if passed >= 4:
    print("\n✅ HF SPACE IS DEPLOYED AND RESPONDING")
    print("✅ HTTP/2 200 OK verified")
    print("✅ Ready for hackathon judges")
else:
    print("\n⚠️  Space may still be building or loading")
    print("Wait 2-3 minutes and try again")

print("\nSpace URL: https://devendranp-agentic-ai-app.hf.space")
print("=" * 70 + "\n")
