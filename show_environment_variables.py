#!/usr/bin/env python3
"""
Environment Variables & API Keys Reference
Shows all required environment variables and how to set them up
"""

import os
import sys

def display_env_vars():
    print("=" * 80)
    print("🔑 REQUIRED ENVIRONMENT VARIABLES & API KEYS")
    print("=" * 80)
    
    print("\n📋 ENVIRONMENT VARIABLES CURRENTLY SET:")
    print("-" * 80)
    
    # List of variables to check
    vars_to_check = [
        "OPENAI_API_KEY",
        "API_BASE_URL",
        "MODEL_NAME",
        "HF_TOKEN",
        "API_KEY",
    ]
    
    found_vars = {}
    for var in vars_to_check:
        value = os.getenv(var)
        if value:
            # Mask the actual value for security
            masked = value[:10] + "..." if len(value) > 10 else value
            found_vars[var] = masked
            print(f"✅ {var:20} = {masked}")
        else:
            print(f"❌ {var:20} = (not set)")
    
    print("\n" + "=" * 80)
    print("📚 REQUIRED ENVIRONMENT VARIABLES FOR PROJECT")
    print("=" * 80)
    
    config = {
        "1. API_BASE_URL": {
            "purpose": "API endpoint URL",
            "type": "String (URL)",
            "default": "https://api.openai.com/v1",
            "options": [
                "https://api.openai.com/v1  (OpenAI)",
                "https://router.huggingface.co/v1  (HuggingFace Router)",
            ],
            "required": "✅ YES (has default)"
        },
        "2. MODEL_NAME": {
            "purpose": "LLM model identifier",
            "type": "String",
            "default": "gpt-3.5-turbo",
            "options": [
                "gpt-3.5-turbo  (OpenAI)",
                "gpt-4  (OpenAI)",
                "Qwen/Qwen2.5-72B-Instruct  (HuggingFace)",
                "meta-llama/Llama-2-70b  (HuggingFace)",
            ],
            "required": "✅ YES (has default)"
        },
        "3. HF_TOKEN": {
            "purpose": "Authentication token for API",
            "type": "String (API Token/Key)",
            "default": "Empty (no default)",
            "options": [
                "sk-proj-... (OpenAI API key)",
                "hf_... (HuggingFace token)",
            ],
            "required": "⚠️ OPTIONAL (but needed for LLM features)"
        },
        "4. API_KEY": {
            "purpose": "Fallback for HF_TOKEN",
            "type": "String (API Token/Key)",
            "default": "Empty (no default)",
            "options": [
                "sk-... (OpenAI key)",
                "hf_... (HF token)",
            ],
            "required": "⚠️ OPTIONAL (alternative to HF_TOKEN)"
        },
    }
    
    for var_name, details in config.items():
        print(f"\n{var_name}")
        print(f"  Purpose:  {details['purpose']}")
        print(f"  Type:     {details['type']}")
        print(f"  Required: {details['required']}")
        print(f"  Default:  {details['default']}")
        print(f"  Options:")
        for option in details['options']:
            print(f"    • {option}")
    
    print("\n" + "=" * 80)
    print("🔐 HOW TO GET API KEYS")
    print("=" * 80)
    
    print("\n1️⃣  OPENAI API KEY (sk-...)")
    print("-" * 80)
    print("   Source: https://platform.openai.com/api-keys")
    print("   Steps:")
    print("     1. Go to OpenAI platform (https://platform.openai.com/)")
    print("     2. Sign up or log in")
    print("     3. Navigate to API keys section")
    print("     4. Create a new secret key")
    print("     5. Copy and save the key (starts with 'sk-')")
    print("   Pricing: Pay-as-you-go (token-based)")
    print("   Usage: For gpt-3.5-turbo and gpt-4 models")
    
    print("\n2️⃣  HUGGINGFACE TOKEN (hf_...)")
    print("-" * 80)
    print("   Source: https://huggingface.co/settings/tokens")
    print("   Steps:")
    print("     1. Go to HuggingFace website (https://huggingface.co/)")
    print("     2. Sign up or log in")
    print("     3. Go to Settings > Access Tokens")
    print("     4. Create a new token (with 'read' permission)")
    print("     5. Copy the token (starts with 'hf_')")
    print("   Pricing: FREE (community models)")
    print("   Usage: For open-source models via HF Router")
    
    print("\n" + "=" * 80)
    print("⚙️  HOW TO SET ENVIRONMENT VARIABLES")
    print("=" * 80)
    
    print("\n✅ OPTION 1: Using .env File (Recommended for development)")
    print("-" * 80)
    print("   Current .env.example in project:")
    print("""
   # Copy .env.example to .env and fill in your values:
   
   # Option 1: Use HuggingFace (Free, recommended for HF Spaces)
   API_BASE_URL=https://router.huggingface.co/v1
   MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
   
   # Option 2: Use OpenAI (Paid, requires API key)
   # API_BASE_URL=https://api.openai.com/v1
   # MODEL_NAME=gpt-3.5-turbo
   # HF_TOKEN=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   """)
    
    print("\n✅ OPTION 2: Windows Command Line")
    print("-" * 80)
    print("   PowerShell:")
    print("     $env:API_BASE_URL='https://api.openai.com/v1'")
    print("     $env:MODEL_NAME='gpt-3.5-turbo'")
    print("     $env:HF_TOKEN='sk-your-api-key-here'")
    print("     python inference.py --task easy --episodes 1")
    print()
    print("   CMD:")
    print("     set API_BASE_URL=https://api.openai.com/v1")
    print("     set MODEL_NAME=gpt-3.5-turbo")
    print("     set HF_TOKEN=sk-your-api-key-here")
    print("     python inference.py --task easy --episodes 1")
    
    print("\n✅ OPTION 3: HuggingFace Spaces (Production)")
    print("-" * 80)
    print("   1. Create a Space on HuggingFace")
    print("   2. Go to Space Settings > Repository Secrets")
    print("   3. Add these secrets:")
    print("      - API_BASE_URL: https://router.huggingface.co/v1")
    print("      - MODEL_NAME: Qwen/Qwen2.5-72B-Instruct")
    print("      - HF_TOKEN: your-hf-token")
    print("   4. App loads them automatically")
    
    print("\n✅ OPTION 4: Docker Environment")
    print("-" * 80)
    print("   In docker run command:")
    print("     docker run -e API_BASE_URL='https://api.openai.com/v1' \\")
    print("               -e MODEL_NAME='gpt-3.5-turbo' \\")
    print("               -e HF_TOKEN='sk-...' \\")
    print("               my-image:latest")
    
    print("\n✅ OPTION 5: Python Script")
    print("-" * 80)
    print("   import os")
    print("   os.environ['API_BASE_URL'] = 'https://api.openai.com/v1'")
    print("   os.environ['MODEL_NAME'] = 'gpt-3.5-turbo'")
    print("   os.environ['HF_TOKEN'] = 'sk-your-key'")
    print("   # Then run app/inference")
    
    print("\n" + "=" * 80)
    print("📝 WHERE VARIABLES ARE USED IN CODE")
    print("=" * 80)
    
    usage_locations = {
        "app.py": {
            "lines": "17-20",
            "code": """
            API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
            MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
            HF_TOKEN = os.getenv("HF_TOKEN", "")
            """
        },
        "inference.py (CLI)": {
            "lines": "34-38",
            "code": """
            API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
            MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
            HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
            OPENAI_API_KEY = HF_TOKEN
            """
        },
    }
    
    for file, details in usage_locations.items():
        print(f"\n{file} (lines {details['lines']}):")
        print(details['code'])
    
    print("\n" + "=" * 80)
    print("🎯 QUICKSTART WITH ENVIRONMENT VARIABLES")
    print("=" * 80)
    
    print("\n1. Copy template:")
    print("   cp .env.example .env")
    
    print("\n2. Edit .env with your API key:")
    print("   # Windows:")
    print("   notepad .env")
    print("   # Mac/Linux:")
    print("   nano .env")
    
    print("\n3. For HuggingFace (FREE):")
    print("   API_BASE_URL=https://router.huggingface.co/v1")
    print("   MODEL_NAME=Qwen/Qwen2.5-72B-Instruct")
    print("   HF_TOKEN=hf_your-token-from-huggingface")
    
    print("\n4. For OpenAI (PAID):")
    print("   API_BASE_URL=https://api.openai.com/v1")
    print("   MODEL_NAME=gpt-3.5-turbo")
    print("   HF_TOKEN=sk-your-token-from-openai")
    
    print("\n5. Run the inference:")
    print("   python inference.py --task easy --episodes 1 --agent heuristic")
    
    print("\n" + "=" * 80)
    print("📊 CURRENT STATUS")
    print("=" * 80)
    print(f"\nEnvironment Variables Set: {len(found_vars)}/4")
    if found_vars:
        print("Set variables:")
        for var, masked_val in found_vars.items():
            print(f"  ✅ {var}")
    else:
        print("⚠️  No API keys currently set (project still works with heuristic agents)")
    
    print("\n" + "=" * 80)
    print("✅ PROJECT STATUS: Ready to use")
    print("=" * 80)
    print("""
✅ Heuristic Agents: Work WITHOUT API keys (SmartHeuristicAgent, RandomBaselineAgent)
✅ Q-Learning Agent: Works WITHOUT API keys (QLearningAgent)
⚠️  OpenAI Integration: Requires HF_TOKEN or OPENAI_API_KEY to be set
ℹ️  HuggingFace Spaces: Automatically reads environment variables from Repository Secrets
    """)

if __name__ == "__main__":
    display_env_vars()
