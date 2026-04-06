# 📋 ENVIRONMENT VARIABLES QUICK REFERENCE

Your hackathon submission loads 3 required environment variables.

---

## Where They Are Loaded

### app.py (FastAPI Server)

```python
# Line 17-19
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "")
```

### inference.py (Inference Script)

```python
# Line 34-36
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
```

---

## Variable Usage

### API_BASE_URL

- **Purpose**: API endpoint for LLM inference
- **Default**: `https://api.openai.com/v1` (OpenAI)
- **For HF Spaces**: `https://router.huggingface.co/v1`
- **Used by**: OpenAIAgent class in inference.py
- **Code**: src/inference.py line ~120

### MODEL_NAME

- **Purpose**: Model identifier for inference
- **Default**: `gpt-3.5-turbo` (OpenAI)
- **For HF Spaces**: `Qwen/Qwen2.5-72B-Instruct` (or similar)
- **Used by**: OpenAIAgent class for API calls
- **Code**: src/inference.py line ~130

### HF_TOKEN

- **Purpose**: Authentication token for API access
- **Default**: Empty string (fallback to heuristic agent)
- **For HF Spaces**: Your HuggingFace API token
- **Format**: `hf_xxxxxxxxxxxxxxxxxxxx` (HF) or `sk_xxxxxxxx` (OpenAI)
- **Used by**: OpenAIAgent client initialization
- **Code**: src/inference.py line ~105

---

## How to Set Variables

### Local Development

Create `.env` file:

```bash
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
```

Then load it:

```python
from dotenv import load_dotenv
load_dotenv()
```

### HuggingFace Spaces

1. Go to Space Settings
2. Scroll to "Repository secrets"
3. Add each variable:
   - Name: `API_BASE_URL`
   - Value: `https://router.huggingface.co/v1`
   - Save
4. Repeat for MODEL_NAME and HF_TOKEN
5. Rebuild Space

### Docker Container

Pass as environment variables:

```bash
docker run \
  -e API_BASE_URL="https://router.huggingface.co/v1" \
  -e MODEL_NAME="Qwen/Qwen2.5-72B-Instruct" \
  -e HF_TOKEN="hf_xxxx" \
  -p 7860:7860 \
  emergency-response
```

### System Environment

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="hf_xxxx"
python inference.py --task easy
```

---

## Fallback Behavior

If variables are NOT set, the system falls back to:

1. **OpenAI defaults** (inference.py):
   - API_BASE_URL → `https://api.openai.com/v1`
   - MODEL_NAME → `gpt-3.5-turbo`
   - HF_TOKEN → Requires valid OpenAI key

2. **NO fallback** (if token empty):
   - OpenAIAgent initialization fails
   - Automatically switches to SmartHeuristicAgent
   - Inference still runs normally ✅

3. **Heuristic agent always available**:
   - Doesn't require LLM access
   - Works completely offline
   - Returns deterministic scores

---

## Requirement 7 Compliance ✅

Your submission meets Requirement 7:

✅ API_BASE_URL defined in app.py (line 17)
✅ MODEL_NAME defined in app.py (line 18)
✅ HF_TOKEN defined in app.py (line 19)
✅ All loaded via os.getenv() ✓
✅ All variables also in inference.py ✓
✅ Fallback values provided ✓
✅ Compatible with HF Spaces secrets ✓

Verified by: `check_hackathon_requirements.py` → Requirement 7 PASSED ✅

---

## Example Values

### HuggingFace Setup (Recommended)

```
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
HF_TOKEN=hf_1234567890abcdefghijklmnopqrst
```

### OpenAI Setup (Alternative)

```
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
HF_TOKEN=sk_test_1234567890abcdefghijklmnopqrst
```

### Local Testing (No LLM Needed)

```
# Don't set HF_TOKEN - will use heuristic agent
API_BASE_URL=https://router.huggingface.co/v1  # Only for reference
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct           # Only for reference
HF_TOKEN=                                       # Empty - uses fallback
```

---

## Verification

Test that variables are correctly loaded:

```bash
# Check local environment
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API_BASE_URL:', os.getenv('API_BASE_URL')); print('MODEL_NAME:', os.getenv('MODEL_NAME')); print('HF_TOKEN:', 'SET' if os.getenv('HF_TOKEN') else 'NOT SET')"

# Check in running app
curl http://localhost:7860/health  # Returns environment info
```

---

## Support

If environment variables aren't loading:

1. Check `.env` file exists in root directory
2. Verify `from dotenv import load_dotenv` is called
3. For HF Spaces: Check Repository Secrets are added
4. For Docker: Check -e flags are passed correctly
5. For system: Check `echo $API_BASE_URL` shows value

---

🎯 **Status**: All 3 environment variables properly configured and hackathon-compliant ✅
