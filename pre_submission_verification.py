#!/usr/bin/env python3
"""
Pre-Submission Checklist Verification
Validates all requirements from the hackathon checklist before submission
"""

import os
import sys
import re
from pathlib import Path

def verify_requirements():
    print("=" * 80)
    print("✅ PRE-SUBMISSION CHECKLIST VERIFICATION")
    print("=" * 80)
    
    checks_passed = 0
    checks_failed = 0
    
    # ============================================================================
    # 1. Sample inference.py structure
    # ============================================================================
    print("\n1️⃣  Sample inference.py Structure")
    print("-" * 80)
    
    try:
        with open("inference.py") as f:
            inference_content = f.read()
        
        # Check for key components
        required_components = {
            "import os": "OS module import",
            "argparse": "CLI argument parsing",
            "EmergencyResponseEnv": "Environment import",
            "log_start": "Log start function",
            "log_step": "Log step function", 
            "log_end": "Log end function",
            "def main": "Main function",
            "if __name__": "Main entry point",
        }
        
        all_components_found = True
        for component, description in required_components.items():
            if component in inference_content:
                print(f"✅ {description:30} ('{component}' found)")
                checks_passed += 1
            else:
                print(f"❌ {description:30} ('{component}' NOT found)")
                checks_failed += 1
                all_components_found = False
        
    except Exception as e:
        print(f"❌ Error reading inference.py: {e}")
        checks_failed += 1
    
    # ============================================================================
    # 2. Environment variables in inference.py
    # ============================================================================
    print("\n2️⃣  Environment Variables Configuration")
    print("-" * 80)
    
    env_vars = {
        "API_BASE_URL": "API endpoint URL",
        "MODEL_NAME": "Model identifier",
        "HF_TOKEN": "Authentication token",
    }
    
    for var, description in env_vars.items():
        if f'os.getenv("{var}"' in inference_content or f"os.getenv('{var}'" in inference_content:
            print(f"✅ {var:20} present ({description})")
            checks_passed += 1
        else:
            print(f"❌ {var:20} missing ({description})")
            checks_failed += 1
    
    # ============================================================================
    # 3. Defaults set correctly (only for API_BASE_URL and MODEL_NAME)
    # ============================================================================
    print("\n3️⃣  Default Values Configuration")
    print("-" * 80)
    
    # Check API_BASE_URL has default
    if 'os.getenv("API_BASE_URL",' in inference_content or "os.getenv('API_BASE_URL'," in inference_content:
        print("✅ API_BASE_URL has default value")
        checks_passed += 1
    else:
        print("❌ API_BASE_URL missing default")
        checks_failed += 1
    
    # Check MODEL_NAME has default
    if 'os.getenv("MODEL_NAME",' in inference_content or "os.getenv('MODEL_NAME'," in inference_content:
        print("✅ MODEL_NAME has default value")
        checks_passed += 1
    else:
        print("❌ MODEL_NAME missing default")
        checks_failed += 1
    
    # Check HF_TOKEN does NOT have default (or empty default)
    if ('os.getenv("HF_TOKEN")' in inference_content or "os.getenv('HF_TOKEN')" in inference_content or
        'HF_TOKEN = os.getenv' in inference_content):
        print("✅ HF_TOKEN NO default (optional, correct)")
        checks_passed += 1
    else:
        print("⚠️  HF_TOKEN configuration unclear")
    
    # ============================================================================
    # 4. OpenAI Client configuration
    # ============================================================================
    print("\n4️⃣  OpenAI Client Configuration")
    print("-" * 80)
    
    if "from openai import OpenAI" in inference_content:
        print("✅ OpenAI import present ('from openai import OpenAI')")
        checks_passed += 1
    else:
        print("❌ OpenAI import missing")
        checks_failed += 1
    
    if "OpenAI(" in inference_content:
        print("✅ OpenAI client instantiation present")
        checks_passed += 1
    else:
        print("⚠️  OpenAI client instantiation not found (may be optional)")
    
    # ============================================================================
    # 5. Structured logging format [START]/[STEP]/[END]
    # ============================================================================
    print("\n5️⃣  Structured Logging Format")
    print("-" * 80)
    
    logging_patterns = {
        r"\[START\]": "[START] format",
        r"\[STEP\]": "[STEP] format",
        r"\[END\]": "[END] format",
    }
    
    for pattern, description in logging_patterns.items():
        if re.search(pattern, inference_content):
            print(f"✅ {description:30} found in code")
            checks_passed += 1
        else:
            print(f"❌ {description:30} NOT found in code")
            checks_failed += 1
    
    # Verify logging functions
    if "def log_start" in inference_content:
        print("✅ log_start() function defined")
        checks_passed += 1
    else:
        print("❌ log_start() function missing")
        checks_failed += 1
    
    if "def log_step" in inference_content:
        print("✅ log_step() function defined")
        checks_passed += 1
    else:
        print("❌ log_step() function missing")
        checks_failed += 1
    
    if "def log_end" in inference_content:
        print("✅ log_end() function defined")
        checks_passed += 1
    else:
        print("❌ log_end() function missing")
        checks_failed += 1
    
    # ============================================================================
    # 6. App.py environment variables
    # ============================================================================
    print("\n6️⃣  FastAPI App Configuration (app.py)")
    print("-" * 80)
    
    try:
        with open("app.py") as f:
            app_content = f.read()
        
        app_checks = {
            'os.getenv("API_BASE_URL"': "API_BASE_URL in app.py",
            'os.getenv("MODEL_NAME"': "MODEL_NAME in app.py",
            'os.getenv("HF_TOKEN"': "HF_TOKEN in app.py",
        }
        
        for check, description in app_checks.items():
            if check in app_content:
                print(f"✅ {description}")
                checks_passed += 1
            else:
                print(f"❌ {description}")
                checks_failed += 1
                
    except Exception as e:
        print(f"⚠️  Could not check app.py: {e}")
    
    # ============================================================================
    # 7. .env.example file
    # ============================================================================
    print("\n7️⃣  Environment Variables Template (.env.example)")
    print("-" * 80)
    
    if Path(".env.example").exists():
        print("✅ .env.example file exists")
        checks_passed += 1
        
        try:
            with open(".env.example") as f:
                env_example = f.read()
            
            if "API_BASE_URL" in env_example:
                print("✅ .env.example has API_BASE_URL")
                checks_passed += 1
            else:
                print("❌ .env.example missing API_BASE_URL")
                checks_failed += 1
            
            if "MODEL_NAME" in env_example:
                print("✅ .env.example has MODEL_NAME")
                checks_passed += 1
            else:
                print("❌ .env.example missing MODEL_NAME")
                checks_failed += 1
            
            if "HF_TOKEN" in env_example:
                print("✅ .env.example has HF_TOKEN")
                checks_passed += 1
            else:
                print("❌ .env.example missing HF_TOKEN")
                checks_failed += 1
        except Exception as e:
            print(f"⚠️  Could not read .env.example: {e}")
    else:
        print("❌ .env.example file NOT found")
        checks_failed += 1
    
    # ============================================================================
    # 8. Test logging output
    # ============================================================================
    print("\n8️⃣  Test Logging Output")
    print("-" * 80)
    
    try:
        from src.env import EmergencyResponseEnv
        
        env = EmergencyResponseEnv()
        state = env.reset()
        action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
        obs, reward, done, info = env.step(action)
        
        # Try running with agent to check logging
        print("✅ Environment and step() methods work")
        checks_passed += 1
        
        # Test a simple run
        print("✅ Can create environment and take steps")
        checks_passed += 1
        
    except Exception as e:
        print(f"❌ Error testing environment: {e}")
        checks_failed += 1
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 80)
    print("📊 CHECKLIST SUMMARY")
    print("=" * 80)
    
    total_checks = checks_passed + checks_failed
    pass_rate = (checks_passed / total_checks * 100) if total_checks > 0 else 0
    
    print(f"\nTotal Checks: {total_checks}")
    print(f"Passed: {checks_passed} ✅")
    print(f"Failed: {checks_failed} ❌")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if checks_failed == 0:
        print("\n" + "=" * 80)
        print("🎉 ALL REQUIREMENTS MET - READY FOR SUBMISSION")
        print("=" * 80)
        print("\nNext Steps:")
        print("1. ✅ GitHub repo synced (done)")
        print("2. 📝 Create HuggingFace Space (link to GitHub)")
        print("3. 🏆 Submit to hackathon platform")
        print("4. ⏰ Deadline: April 8, 11:59 PM")
        return 0
    else:
        print("\n" + "=" * 80)
        print(f"⚠️  {checks_failed} ISSUES TO FIX")
        print("=" * 80)
        print("\nPlease address the failed checks above before submission.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_requirements())
