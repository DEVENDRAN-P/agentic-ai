# 🎯 OPENENV ROUND 1 - SUBMISSION ACTION PLAN

**Your Hackathon Deadline: 8th April 11:59 PM**  
**Team: Future_Hacks** | **Status: Step 2 - Build & Submit**

---

## ⚡ QUICK STATUS CHECK

Your Emergency Response Environment has:

- ✅ 9/9 validation checks passing
- ✅ Multiple agent types implemented
- ✅ Docker support ready
- ✅ Comprehensive documentation

**Now you need to:**

1. Create proper `inference.py` with mandatory log format
2. Deploy to HuggingFace Space (live & runnable)
3. Ensure OpenEnv spec compliance
4. Complete final submission

---

## 📋 STEP-BY-STEP ACTION PLAN

### STEP 1: Create Mandatory inference.py (15 min)

**Location**: Root of your project  
**Requirement**: Must follow exact [START], [STEP], [END] format

First, check your current project structure:

```bash
ls -la inference.py  # Check if it exists
```

If NOT present, create it using the template below.

### STEP 2: Set Up Environment Variables (5 min)

**Required Variables**:

```bash
API_BASE_URL      # LLM endpoint
MODEL_NAME        # Model identifier
HF_TOKEN          # Your HuggingFace token
```

**Set locally**:

```powershell
$env:API_BASE_URL = "https://router.huggingface.co/v1"
$env:MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"
$env:HF_TOKEN = "your-token-here"
```

### STEP 3: Prepare HuggingFace Space (20 min)

1. Go to https://huggingface.co/spaces
2. Create new space
3. Connect to your GitHub repo
4. Ensure `inference.py` runs successfully
5. Space must respond to `reset()` with HTTP 200

### STEP 4: Verify Docker Build (10 min)

```bash
docker build -t emergency-response .
docker run emergency-response python inference.py
```

### STEP 5: Run Final Validation (10 min)

```bash
python -c "
import subprocess
result = subprocess.run(['python', 'inference.py'], capture_output=True, text=True)
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)
print('Return code:', result.returncode)
"
```

### STEP 6: Submit (5 min)

1. Go to hackathon dashboard
2. Fill submission form with:
   - GitHub repo link
   - HuggingFace Space link
   - Brief description
3. Click SUBMIT

---

## 🔧 MANDATORY inference.py TEMPLATE

**Create file**: `c:\Users\LENOVO\OneDrive\Desktop\agent\inference.py`

```python
#!/usr/bin/env python3
"""
MANDATORY OpenEnv Round 1 Inference Script

Required format:
  [START] task=<task_name> env=<env_name> model=<model_name>
  [STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
  [END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn>
"""

import os
import sys
import json
from typing import Optional, List
from src.env import EmergencyResponseEnv
from src.inference import PriorityAgent

# Mandatory environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")
TASK_NAME = os.getenv("TASK_NAME", "easy")

def log_start(task: str, env: str, model: str) -> None:
    """Emit [START] log"""
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    """Emit [STEP] log"""
    error_val = error if error else "null"
    done_val = str(done).lower()
    reward_fmt = f"{reward:.2f}"
    print(f"[STEP] step={step} action={action} reward={reward_fmt} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    """Emit [END] log"""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    success_val = str(success).lower()
    print(f"[END] success={success_val} steps={steps} rewards={rewards_str}", flush=True)

def run_inference(task_name: str = "easy", max_steps: int = 50) -> None:
    """Run inference with mandatory logging format"""

    env_name = "emergency-response-v1"
    all_steps = []
    all_rewards = []
    success = True
    current_step = 0

    try:
        # Initialize environment
        env = EmergencyResponseEnv()
        log_start(task=task_name, env=env_name, model=MODEL_NAME)

        # Reset environment
        obs, info = env.reset()

        # Run episodes
        for episode in range(3):  # Run 3 episodes
            obs, info = env.reset()
            done = False
            episode_reward = 0

            for step in range(max_steps):
                if done:
                    break

                current_step += 1

                # Get action from agent
                agent = PriorityAgent()
                action = agent.get_action(obs, info)

                # Execute step
                obs, reward, done, info = env.step(action)

                # Log step
                action_str = f"ambulance_{action[0]}_emergency_{action[1]}_hospital_{action[2]}"
                log_step(
                    step=current_step,
                    action=action_str,
                    reward=float(reward),
                    done=done,
                    error=None
                )

                all_steps.append(step)
                all_rewards.append(reward)
                episode_reward += reward

        # Log end
        log_end(success=True, steps=current_step, rewards=all_rewards)

    except Exception as e:
        log_end(success=False, steps=current_step, rewards=all_rewards)
        print(f"Error: {str(e)}", file=sys.stderr, flush=True)
        sys.exit(1)
    finally:
        if 'env' in locals():
            env.close()

if __name__ == "__main__":
    task = os.getenv("TASK_NAME", "easy")
    run_inference(task_name=task)
```

---

## ✅ HACKATHON COMPLIANCE CHECKLIST

Before final submission (8th April 11:59 PM):

### Pre-Submission Checks

- [ ] HF Space deployed and live

  ```bash
  curl -i https://your-space.hf.space/reset
  # Expected: HTTP 200
  ```

- [ ] OpenEnv spec compliance

  ```bash
  python -c "
  from src.env import EmergencyResponseEnv
  env = EmergencyResponseEnv()
  print('Has reset:', hasattr(env, 'reset'))
  print('Has step:', hasattr(env, 'step'))
  print('Has close:', hasattr(env, 'close'))
  "
  ```

- [ ] Dockerfile builds

  ```bash
  docker build -t emergency-response . --no-cache
  ```

- [ ] inference.py reproduces

  ```bash
  python inference.py 2>&1 | head -20
  # Should show [START], [STEP], [END] logs
  ```

- [ ] 3+ tasks with graders

  ```bash
  python -c "
  from src.env import EmergencyResponseEnv
  env = EmergencyResponseEnv()
  print('Available tasks:', ['easy', 'medium', 'hard'])
  "
  ```

- [ ] Scores in 0.0-1.0 range
  ```bash
  python -c "
  from src.graders import compute_graders
  import numpy as np
  for reward in [0, 0.5, 1.0]:
      scores = compute_graders(reward, 0, 0)
      print(f'Reward {reward}: {scores}')
      assert all(0 <= s <= 1 for s in scores.values())
  print('✅ All scores valid')
  "
  ```

### Infrastructure Requirements

- [ ] Runtime < 20 minutes

  ```bash
  time python inference.py
  ```

- [ ] Runs on 2vCPU, 8GB RAM machine
  - Docker limit: 2 cores

  ```bash
  docker run --cpus="2" --memory="8g" emergency-response
  ```

- [ ] No hardcoded paths
  - Search: `C:\Users\`, `/home/user/`, etc.
  ```bash
  grep -r "C:\\Users" . --exclude-dir=.venv
  # Should return: nothing
  ```

---

## 📝 SUBMISSION CHECKLIST

**Before clicking SUBMIT on dashboard:**

### Code Quality

- [ ] No syntax errors

  ```bash
  python -m py_compile src/*.py inference.py
  ```

- [ ] All imports work

  ```bash
  python -c "from src.env import *; from src.inference import *"
  ```

- [ ] README complete and clear
  - Problem description ✓
  - Environment setup ✓
  - Action/observation spaces ✓
  - How to run ✓
  - Example output ✓

### Deployment

- [ ] GitHub repo public and has all files
- [ ] HF Space linked to GitHub repo
- [ ] Dockerfile in root directory
- [ ] inference.py in root directory
- [ ] requirements.txt with all dependencies
- [ ] .gitignore excludes .venv, **pycache**, etc.

### Testing

- [ ] Run validation locally

  ```bash
  python validate_hackathon.py
  # Expected: 9/9 PASS
  ```

- [ ] Test inference.py

  ```bash
  python inference.py > test_output.txt
  grep "^\[START\]" test_output.txt  # Should exist
  grep "^\[STEP\]" test_output.txt   # Should exist
  grep "^\[END\]" test_output.txt    # Should exist
  ```

- [ ] Test Docker
  ```bash
  docker build -t test .
  docker run test python validate_hackathon.py
  ```

---

## 🚨 CRITICAL DEADLINES

| Date                   | Milestone                 | Status      |
| ---------------------- | ------------------------- | ----------- |
| Now                    | Build environment         | ✅ DONE     |
| Now - 25th March       | Prepare                   | IN PROGRESS |
| 25th March - 8th April | Round 1 (submission open) | UPCOMING    |
| **8th April 11:59 PM** | **SUBMISSION DEADLINE**   | ⏰ CRITICAL |
| 10th April             | Results announced         | Future      |
| 25-26th April          | Finale                    | Future      |

---

## 🎯 NEXT IMMEDIATE ACTIONS (DO THIS NOW)

### Action 1: Create inference.py (10 min)

```bash
cd c:\Users\LENOVO\OneDrive\Desktop\agent
# Copy the template above into inference.py
```

### Action 2: Test it works (5 min)

```bash
$env:API_BASE_URL = "https://router.huggingface.co/v1"
python inference.py 2>&1 | head -5
# Should show: [START] task=easy env=emergency-response-v1 model=...
```

### Action 3: Prepare HF Space (15 min)

1. Create Space on huggingface.co/spaces
2. Push repo
3. Verify it deploys

### Action 4: Final validation (10 min)

```bash
python validate_hackathon.py
python inference.py
docker build -t test .
```

### Action 5: Submit (5 min)

Go to hackathon dashboard → Submit Assessment → Fill form → SUBMIT

---

## ❓ COMMON QUESTIONS

**Q: What if I don't have HF_TOKEN?**
A: Generate one at https://huggingface.co/settings/tokens

**Q: Can I use local model instead of API?**
A: API_BASE_URL must be set, but you can point to local server

**Q: What if inference.py takes > 20 min?**
A: Reduce max_steps or episodes, optimize agent logic

**Q: Can I change the [START]/[STEP]/[END] format?**
A: NO. Any deviation=disqualification. Follow exactly.

**Q: Team lead must submit?**
A: YES. Only DEVENDRAN P can click final submit

---

## 📞 SUPPORT

**Hackathon Help**: help_openenvhackathon@scaler.com  
**Discord**: Join Discord community for announcements  
**Deadline**: 8th April 11:59 PM (UTC/IST?)

---

## ✨ YOU'RE READY!

Your environment:

- ✅ Solves real-world problem (Emergency Response)
- ✅ Has sophisticated reward system
- ✅ Supports multiple difficulty levels
- ✅ Includes multiple agent strategies
- ✅ Has comprehensive testing

**Just need to:**

1. Create inference.py ✓
2. Deploy to HF Space ✓
3. Verify compliance ✓
4. Submit ✓

**Time to submission: 50 minutes of work**

---

**Version**: OpenEnv Round 1 Edition  
**Last Updated**: April 3, 2026  
**Next Action**: Create inference.py NOW
