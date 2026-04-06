# 🚀 QUICK DEPLOY GUIDE: Push to HF Space

Your local code is correct. Follow these 3 simple steps to deploy:

---

## STEP 1: Clone Your Space Repository

```powershell
cd C:\Users\LENOVO\Desktop
git clone https://huggingface.co/spaces/devendranp/agentic-ai-app
cd agentic-ai-app
```

Or if you already have it:

```powershell
cd path/to/your/space-repo
git pull  # Get latest
```

---

## STEP 2: Copy Updated Files

From your agent project, copy these files:

```powershell
# Copy the new app.py
Copy-Item C:\Users\LENOVO\OneDrive\Desktop\agent\app.py . -Force

# Copy other key files (already there but verify)
Copy-Item C:\Users\LENOVO\OneDrive\Desktop\agent\requirements.txt . -Force
Copy-Item C:\Users\LENOVO\OneDrive\Desktop\agent\Dockerfile . -Force
Copy-Item C:\Users\LENOVO\OneDrive\Desktop\agent\inference.py . -Force

# Copy src/ folder
Copy-Item C:\Users\LENOVO\OneDrive\Desktop\agent\src\ . -Recurse -Force
```

---

## STEP 3: Push to HF (Git)

```powershell
cd path/to/space-repo

# Check what changed
git status

# Add the updated files
git add app.py Dockerfile requirements.txt inference.py
git add src/*
git add .

# Commit
git commit -m "Add /ping /validate /reset /health endpoints (Requirement 2-3-7)"

# Push to HF (will trigger auto-rebuild)
git push

# HF will rebuild in 2-5 minutes
```

---

## STEP 4: Verify Deployment

Wait 3-5 minutes for HF to rebuild, then run:

```powershell
cd C:\Users\LENOVO\OneDrive\Desktop\agent
python test_space_deployment.py
```

Expected output:

```
✅ ROOT - Health check              HTTP 200 OK
✅ PING - Requirement 2             HTTP 200 OK
✅ VALIDATE - Requirement 3         HTTP 200 OK
✅ RESET - Requirement 2            HTTP 200 OK
✅ HEALTH - Service health          HTTP 200 OK
✅ RUN - Requirement 5              HTTP 200 OK

✅ ALL ENDPOINTS DEPLOYED
```

---

## Alternative: Use HF Web Interface

If you prefer not to use Git:

1. Go to: https://huggingface.co/spaces/devendranp/agentic-ai-app
2. Click "Files" tab
3. Click "Edit" on app.py
4. Replace with new content from your local app.py
5. Click "Commit"
6. HF auto-rebuilds

---

## Quick Status Check

**Before push:**

```
✅ / endpoint              200 OK
❌ /ping endpoint          404 Not Found (NEEDS FIX)
❌ /validate endpoint      404 Not Found (NEEDS FIX)
❌ /reset endpoint         404 Not Found (NEEDS FIX)
✅ /run endpoint           200 OK
❌ /health endpoint        404 Not Found (NEEDS FIX)
```

**After push + rebuild:**

```
✅ All 6 endpoints         200 OK ✓
```

---

## Troubleshooting

### Git push fails: "Could not read Username"

→ You need HF credentials
→ Create HF token: https://huggingface.co/settings/tokens
→ Use token as password when prompted

### HF still shows old code

→ Wait 5+ minutes (HF cache)
→ Try different browser/incognito
→ Check Space logs for build errors

### App crashes after push

→ Check Space logs for Python errors
→ Verify requirements.txt has all packages
→ Check app.py imports are correct

---

## Done!

Once rebuilt, all 10 hackathon requirements will pass ✅

Your Space will be ready for judges to test:

- https://devendranp-agentic-ai-app.hf.space/ping (200 OK)
- https://devendranp-agentic-ai-app.hf.space/validate (200 OK)
- https://devendranp-agentic-ai-app.hf.space/run (200 OK)
