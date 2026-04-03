# 🤗 HUGGING FACE SPACES DEPLOYMENT GUIDE

**Deploy your Emergency Response Environment to Hugging Face Spaces**

---

## 📋 WHAT YOU'LL GET

- ✅ Free cloud hosting
- ✅ Public demo URL
- ✅ API endpoint for judges
- ✅ Automatic Docker deployment
- ✅ Live inference capability

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `emergency-response-env` or similar
3. Clone to local:

   ```bash
   git clone https://github.com/YOUR_USERNAME/emergency-response-env.git
   cd emergency-response-env
   ```

4. Copy all project files:

   ```bash
   # Copy src/, tests/, configs/, Dockerfile, requirements.txt, README.md
   cp -r c:\Users\LENOVO\OneDrive\Desktop\agent\* .
   ```

5. Push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit: Emergency Response Environment"
   git push origin main
   ```

✅ **GitHub repo created and pushed**

---

### Step 2: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Space name**: `emergency-response-env`
   - **License**: Apache 2.0 (or your choice)
   - **Space SDK**: Docker
   - **Visibility**: Public

4. Click **"Create Space"**

✅ **Hugging Face Space created**

---

### Step 3: Connect GitHub Repository

1. In your new Space, click **"Settings"** (⚙️ icon)
2. Find **"Repository linked to"**
3. Link to your GitHub repo:

   ```
   https://github.com/YOUR_USERNAME/emergency-response-env
   ```

4. Click **"Sync with GitHub"**

✅ **Repository connected**

---

### Step 4: Configure for Hugging Face

Your Dockerfile already works! HF Spaces will:

1. Pull your repo
2. Build Docker image
3. Run your container
4. Expose port 7860

✅ **Automatic deployment starts**

---

### Step 5: Wait for Deployment

Hugging Face will build and deploy. Check:

- **Space URL**: `https://huggingface.co/spaces/YOUR_USERNAME/emergency-response-env`
- **Build Status**: See logs while building

💡 **First build takes 5-10 minutes**

---

### Step 6: Test Your Space

Once deployed, your Space will show output showing the environment running.

For interactive API (optional), create `app.py`:

```python
from flask import Flask, request, jsonify
from src.env import EmergencyResponseEnv
from src.inference import run_inference
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Online", "message": "Emergency Response Environment"})

@app.route("/validate", methods=["GET"])
def validate():
    """Health check"""
    try:
        env = EmergencyResponseEnv("easy")
        state = env.reset()
        env.state()
        return jsonify({"status": "OK", "message": "Environment operational"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)})

@app.route("/run", methods=["POST"])
def run_inference_api():
    """Run inference with custom parameters"""
    try:
        data = request.get_json()
        task = data.get("task", "easy")
        episodes = data.get("episodes", 2)

        result = run_inference(
            task_difficulty=task,
            num_episodes=episodes,
            agent_type="heuristic",
            use_open_env_format=True
        )

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
```

---

## 📊 DEPLOYMENT CHECKLIST

- [ ] GitHub repo created
- [ ] Code pushed to GitHub
- [ ] Hugging Face account created
- [ ] Space created (Docker)
- [ ] GitHub linked to Space
- [ ] Deployment completed (watch logs)
- [ ] Space URL accessible
- [ ] Test endpoint working

---

## 🔗 SUBMISSION LINKS

Once deployed, you'll have:

```
GitHub Repository: https://github.com/YOUR_USERNAME/emergency-response-env
Hugging Face Space: https://huggingface.co/spaces/YOUR_USERNAME/emergency-response-env
```

---

## 📝 WHAT JUDGES WILL SEE

### On your Space page:

- ✅ Project description
- ✅ Environment running
- ✅ Output from inference
- ✅ Link to GitHub repo
- ✅ README documentation

### Judge Testing:

```bash
# Judges can see your code
git clone https://github.com/YOUR_USERNAME/emergency-response-env
cd emergency-response-env
python validate_hackathon.py

# Expected: 9/9 PASSED ✅
```

---

## 💡 ADVANCED: Add Web Interface

Create `interface.py` for gradio web UI:

```python
import gradio as gr
from src.env import EmergencyResponseEnv
from src.inference import run_inference

def run_demo(task, episodes):
    result = run_inference(
        task_difficulty=task,
        num_episodes=int(episodes),
        agent_type="heuristic",
        verbose=False
    )

    stats = result["statistics"]["final_score"]
    output = f"""
    Task: {task}
    Episodes: {episodes}
    Average Score: {stats['mean']:.3f}
    Score Range: [{stats['min']:.3f}, {stats['max']:.3f}]
    """
    return output

interface = gr.Interface(
    fn=run_demo,
    inputs=[
        gr.Dropdown(["easy", "medium", "hard"]),
        gr.Number(value=5, label="Episodes")
    ],
    outputs="text",
    title="Emergency Response Environment",
    description="AI agent training for emergency response optimization"
)

interface.launch()
```

Install: `pip install gradio`

---

## 🎯 FINAL SUBMISSION FORMAT

When submitting to hackathon, provide:

````markdown
# Emergency Response Environment

## Problem

Optimize emergency response by assigning ambulances to emergencies
and selecting hospitals efficiently.

## Submission Links

- **GitHub Repository**: https://github.com/[USERNAME]/emergency-response-env
- **Hugging Face Space**: https://huggingface.co/spaces/[USERNAME]/emergency-response-env
- **Live Demo**: [Your Space URL]

## How to Validate

```bash
git clone [YOUR_REPO_URL]
cd emergency-response-env
python validate_hackathon.py
# Expected: 9/9 PASSED
```
````

## Features

- ✅ OpenEnv compliant environment
- ✅ 5 advanced agent types
- ✅ Curriculum learning demonstration
- ✅ Professional testing & validation
- ✅ Docker deployment ready
- ✅ Live inference capability

## Quick Start

```bash
# Run validation
python validate_hackathon.py

# Run demo
python -m src.advanced_inference --mode curriculum --episodes 20

# Run with Docker
docker build -t emergency-response .
docker run emergency-response
```

```

---

## ✅ DEPLOYMENT CHECKLIST (FINAL)

### Before Submission
- [ ] GitHub repo created and public
- [ ] All code committed and pushed
- [ ] Hugging Face Space linked
- [ ] Space builds successfully
- [ ] Space runs without errors
- [ ] URL is public and accessible
- [ ] README visible on Space

### Verification
- [ ] Judges can clone your repo
- [ ] validate_hackathon.py runs (9/9 PASS)
- [ ] Demo script runs successfully
- [ ] Docker builds and runs
- [ ] Output format is correct

---

## 🚨 TROUBLESHOOTING

### Space won't build
1. Check GitHub actions logs
2. Verify all files are committed
3. Ensure Dockerfile is valid
4. Check requirements.txt

### "Module not found" error
1. Ensure all imports use relative paths
2. Check that src/__init__.py exists
3. Verify requirements.txt is complete

### Space times out
1. Increase Space resources (if available)
2. Reduce episodes in default command
3. Optimize inference speed

---

## 🎉 AFTER DEPLOYMENT

### You'll have:
✅ Public GitHub repository
✅ Live Hugging Face Space
✅ Working demo for judges
✅ Verified validation script
✅ Professional submission

### Share with judges:
- GitHub repo link
- Space URL
- Validation script command

---

## 📞 SUPPORT LINKS

- GitHub Help: https://docs.github.com/
- HF Spaces Docs: https://huggingface.co/docs/hub/spaces
- Docker Docs: https://docs.docker.com/
- PyYAML Docs: https://pyyaml.org/

---

**Next**: See `SUBMISSION_FORMAT.md` for final submission template

**Status**: Ready for deployment ✅
```
