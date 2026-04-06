# 🔑 ENVIRONMENT VARIABLES SETUP GUIDE

This guide covers Hackathon Requirement 7: Environment variables configuration

---

## Required Variables

Your HuggingFace Space settings MUST have these 3 variables:

```
API_BASE_URL      = https://router.huggingface.co/v1
MODEL_NAME        = Qwen/Qwen2.5-72B-Instruct
HF_TOKEN          = hf_xxxxxxxxxxxxxxxxxxxx
```

---

## STEP 1: Get Your HuggingFace Token

1. Go to: https://huggingface.co/settings/tokens
2. Log in with your HuggingFace account
3. Click "New token"
4. Name: "hackathon-emergency-response"
5. Type: "Read" (sufficient for inference)
6. Copy the token (looks like `hf_xxxxxxxxxxxxxxxxxxxxxxxx`)

---

## STEP 2: Create HuggingFace Space

1. Go to: https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - Space name: `emergency-response-ai` (or your preference)
   - License: MIT (or choose)
   - **Space SDK: Docker** ⭐ Important
   - Visibility: Public (for hackathon)
4. Click "Create Space"

---

## STEP 3: Add Environment Variables to Space

In your HF Space dashboard:

1. Click "Settings" (right side)
2. Scroll to "Repository secrets"
3. Add 3 secrets:

   **Secret 1:**
   - Name: `API_BASE_URL`
   - Value: `https://router.huggingface.co/v1`
   - ✅ Add secret

   **Secret 2:**
   - Name: `MODEL_NAME`
   - Value: `Qwen/Qwen2.5-72B-Instruct`
   - ✅ Add secret

   **Secret 3:**
   - Name: `HF_TOKEN`
   - Value: `hf_xxxxxxxxxxxxxxxxxxxx` (your token from Step 1)
   - ✅ Add secret

All 3 secrets should now appear in the list.

---

## STEP 4: Push Code to HF Space

Clone the Space repository:

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/emergency-response-ai
cd emergency-response-ai
```

Copy all project files:

```bash
cp -r /path/to/agent/* .
```

Push to HF:

```bash
git add .
git commit -m "Initial hackathon submission"
git push
```

HF Spaces will:

1. Auto-detect Dockerfile
2. Build the Docker image
3. Deploy the Space
4. Available in ~5-10 minutes

---

## STEP 5: Verify Deployment

Once deployed, test these endpoints:

1. **Health check:**

   ```
   https://YOUR_USERNAME-emergency-response-ai.hf.space/
   ```

   Should return 200 with status: "running"

2. **Automated ping (Requirement 2):**

   ```
   https://YOUR_USERNAME-emergency-response-ai.hf.space/ping
   ```

   Should return 200 with state keys

3. **Reset environment (Requirement 2):**

   ```
   https://YOUR_USERNAME-emergency-response-ai.hf.space/reset/easy
   ```

   Should return valid state for easy task

4. **Validation (Requirement 3):**

   ```
   https://YOUR_USERNAME-emergency-response-ai.hf.space/validate
   ```

   Should return: `"openenv_compliance": "PASSED"`

5. **Run inference (Requirement 5):**
   ```
   https://YOUR_USERNAME-emergency-response-ai.hf.space/run?task=easy&episodes=1
   ```
   Should execute and return output from inference.py

---

## Troubleshooting

### ❌ Docker build fails

- Check Dockerfile is at root: `./Dockerfile`
- Verify requirements.txt exists
- Check for syntax errors

### ❌ Environment variables not loading

- Go to Space Settings → Repository secrets
- Verify all 3 variables are added
- Wait 2-3 minutes for cache to refresh
- Rebuild Space (Settings → Rebuild)

### ❌ /ping returns 500 error

- Check HF_TOKEN is correct and valid
- Verify it has "Read" permission
- Check API_BASE_URL format is exactly: `https://router.huggingface.co/v1`
- Check MODEL_NAME format, e.g.: `Qwen/Qwen2.5-72B-Instruct`

### ❌ Inference runs but returns empty

- Check inference.py is in root directory
- Verify [START], [STEP], [END] logs are being printed
- Check app.py /run endpoint captures stdout

---

## Local Testing (Before Deployment)

### Test with local environment variables

1. Create `.env` file in project root:

   ```
   API_BASE_URL=https://router.huggingface.co/v1
   MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
   ```

2. Test requirements:

   ```bash
   python check_hackathon_requirements.py
   ```

   Should show: ✅ ALL REQUIREMENTS PASSED (10/10)

3. Test FastAPI locally:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 7860
   ```

4. In another terminal, test endpoints:

   ```bash
   curl http://localhost:7860/ping
   curl http://localhost:7860/validate
   curl http://localhost:7860/run?task=easy&episodes=1
   ```

5. Test Docker build:
   ```bash
   docker build -t emergency-response .
   docker run -p 7860:7860 employment-response
   ```
   Should start on port 7860 without errors

---

## What Judges Will See

When judges test your submission:

1. **Automated system hits:** `https://your-space.hf.space/ping`
   - Expected: 200 status
   - Expected: `reset()` called successfully

2. **Validation check:** `https://your-space.hf.space/validate`
   - Expected: All OpenEnv compliance checks pass

3. **Manual testing:** `https://your-space.hf.space/run`
   - Expected: Inference runs
   - Expected: [START] [STEP] [END] logs present
   - Expected: Scores in [0.0, 1.0]

---

## Environment Variable Reference

### HuggingFace Router (Recommended)

```
API_BASE_URL = https://router.huggingface.co/v1
MODEL_NAME = Qwen/Qwen2.5-72B-Instruct  (or other HF models)
HF_TOKEN = hf_xxxxxxxx
```

Available models on HF:

- `Qwen/Qwen2.5-72B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `meta-llama/Llama-2-70b-chat-hf`

### OpenAI (Alternative)

```
API_BASE_URL = https://api.openai.com/v1
MODEL_NAME = gpt-3.5-turbo  (or gpt-4, etc)
HF_TOKEN = sk_xxxxxxxx (OpenAI API key)
```

### Azure OpenAI (Alternative)

```
API_BASE_URL = https://<resource>.openai.azure.com/
MODEL_NAME = <deployment-name>
HF_TOKEN = <azure-api-key>
```

---

## Compliance Verification

Before submitting, verify:

✅ All 3 environment variables defined
✅ Variables passed as Repository Secrets in HF Spaces
✅ run `python check_hackathon_requirements.py` locally → 10/10 pass
✅ Test /ping endpoint → returns 200
✅ Test /validate endpoint → all checks pass
✅ Test /run endpoint → inference completes
✅ Dockerfile builds locally without errors

---

## Final Checklist

- [ ] HF Account created
- [ ] HF Token generated
- [ ] HF Space created with Docker SDK
- [ ] 3 Repository Secrets added (API_BASE_URL, MODEL_NAME, HF_TOKEN)
- [ ] Code pushed to Space repo
- [ ] Space auto-built successfully
- [ ] /ping endpoint responds 200
- [ ] /validate endpoint passes
- [ ] /run endpoint executes
- [ ] ready to submit

**Status: READY FOR HACKATHON JUDGES** ✨
