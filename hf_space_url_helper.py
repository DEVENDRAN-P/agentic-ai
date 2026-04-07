#!/usr/bin/env python3
"""
HuggingFace Space URL Converter & Validator
Converts full Space URL to the required submission format
"""

print("=" * 80)
print("🤗 HUGGINGFACE SPACE URL CONVERTER")
print("=" * 80)

print("\n📍 PROVIDED URL:")
print("-" * 80)
provided_url = "https://devendranp-agentic-ai-app.hf.space/"
print(f"Raw: {provided_url}")

print("\n🔍 URL ANALYSIS:")
print("-" * 80)

# Parse the URL
# Format: https://[owner]-[space-name].hf.space/
if ".hf.space/" in provided_url:
    # Extract the part before .hf.space/
    subdomain = provided_url.replace("https://", "").split(".hf.space/")[0]
    print(f"Subdomain: {subdomain}")
    
    # The subdomain format is: owner-space-name (separated by first hyphen after owner)
    # devendranp-agentic-ai-app -> owner: devendranp, space: agentic-ai-app
    parts = subdomain.split("-", 1)  # Split only on first hyphen
    
    owner = parts[0]
    space_name = parts[1] if len(parts) > 1 else "unknown"
    
    print(f"Owner: {owner}")
    print(f"Space Name: {space_name}")
    
    # Construct proper URL
    proper_url = f"https://huggingface.co/spaces/{owner}/{space_name}"
    
    print("\n" + "=" * 80)
    print("✅ CORRECT SUBMISSION URL FORMAT")
    print("=" * 80)
    print(f"\n{proper_url}\n")
    
    print("=" * 80)
    print("📋 SUBMISSION CHECKLIST")
    print("=" * 80)
    
    print("""
✅ REQUIRED FORMATS AT SUBMISSION:

When submitting to the hackathon platform, provide:

1. GitHub Repository URL:
   https://github.com/DEVENDRAN-P/agentic-ai

2. HuggingFace Spaces URL (from above):
   https://huggingface.co/spaces/devendranp/agentic-ai-app

3. Team: Future_Hacks

4. Description: Smart Emergency Response Environment - OpenEnv Round 1

════════════════════════════════════════════════════════════════════════════════

⚠️  IMPORTANT: Use the CORRECT FORMAT for HF Space URL
   ✅ CORRECT:   https://huggingface.co/spaces/devendranp/agentic-ai-app
   ❌ WRONG:     https://devendranp-agentic-ai-app.hf.space/ (this is the app URL)

The hackathon platform specifically requires:
   https://huggingface.co/spaces/[owner]/[space-name]

════════════════════════════════════════════════════════════════════════════════
    """)
    
    print("\n✅ READY FOR SUBMISSION")
    print("=" * 80)
    print(f"""
Your HuggingFace Space is live at:
  App URL: https://devendranp-agentic-ai-app.hf.space/
  Space URL: {proper_url}

Submission deadline: April 8, 11:59 PM

Next: Go to hackathon platform and submit both URLs!
    """)

else:
    print("❌ Could not parse URL format")
