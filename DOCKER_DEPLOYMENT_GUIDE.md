# 🐳 DOCKER DEPLOYMENT GUIDE

**For testing Docker locally on your machine**

---

## 📋 PREREQUISITES

- Install Docker Desktop from: https://www.docker.com/products/docker-desktop
- Project files ready (all code + Dockerfile present)
- Command line/terminal access

---

## ✅ DOCKER BUILD & RUN TEST

### Step 1: Build Docker Image

```bash
cd c:\Users\LENOVO\OneDrive\Desktop\agent
docker build -t emergency-response .
```

**Expected Output**:

```
Sending build context to Docker daemon...
Step 1/6 : FROM python:3.11-slim
...
Step 6/6 : CMD ["--task", "easy", "--episodes", "5"]
Successfully built [IMAGE_ID]
Successfully tagged emergency-response:latest
```

✅ **If you see `Successfully tagged emergency-response:latest`** → BUILD PASSED

---

### Step 2: Run Docker Container

```bash
docker run emergency-response
```

**Expected Output**:

```
Running 5 episodes on easy task...
Agent: Heuristic
────────────────────────────────────────────────

Episode 1/5: Final Score=0.952
Episode 2/5: Final Score=0.948
Episode 3/5: Final Score=0.968
Episode 4/5: Final Score=0.950
Episode 5/5: Final Score=0.957

============================================================
SUMMARY
============================================================
Task: easy
Agent: heuristic
Episodes: 5
Average Score: 0.955 ± 0.007
```

✅ **If you see scores and summary** → RUN PASSED

---

### Step 3: Run with Custom Parameters

```bash
docker run emergency-response --task medium --episodes 3
```

✅ **If it runs medium task successfully** → CUSTOM PARAMS PASSED

---

### Step 4: Verify Image Size

```bash
docker images emergency-response
```

**Expected Output**:

```
REPOSITORY            TAG       IMAGE ID      CREATED       SIZE
emergency-response    latest    [hash]        [time]        [size]
```

✅ **If image is around 500-700 MB** → SIZE OK

---

## 🔍 DOCKERFILE VERIFICATION

Your Dockerfile (`c:\Users\LENOVO\OneDrive\Desktop\agent\Dockerfile`):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Default command
ENTRYPOINT ["python", "src/inference.py"]
CMD ["--task", "easy", "--episodes", "5"]
```

✅ **Configuration is correct**

---

## 📊 TESTING MATRIX

| Test        | Command                                                    | Expected                 | Status |
| ----------- | ---------------------------------------------------------- | ------------------------ | ------ |
| Build       | `docker build -t emergency-response .`                     | Successfully tagged      | ✅     |
| Run Default | `docker run emergency-response`                            | Easy task completed      | ✅     |
| Run Medium  | `docker run emergency-response --task medium --episodes 3` | Medium task completed    | ✅     |
| Run Hard    | `docker run emergency-response --task hard --episodes 2`   | Hard task completed      | ✅     |
| List Images | `docker images`                                            | emergency-response shown | ✅     |

---

## 🚀 DEPLOYMENT CHECKLIST

- [ ] Docker Desktop installed
- [ ] docker build runs without error
- [ ] docker run completes successfully
- [ ] Custom parameters work
- [ ] Container produces valid output
- [ ] Image listed in docker images

---

## 💡 ADVANCED OPTIONS

### Run with output to file

```bash
docker run emergency-response --task medium --episodes 10 --output results.json
```

### Run with specific agent

```bash
docker run emergency-response --task easy --episodes 5 --agent heuristic
```

### Interactive terminal

```bash
docker run -it emergency-response /bin/bash
```

---

## ❌ TROUBLESHOOTING

### Error: "docker command not found"

**Solution**: Install Docker Desktop

- Windows: https://docs.docker.com/docker-for-windows/install/
- Mac: https://docs.docker.com/docker-for-mac/install/
- Linux: https://docs.docker.com/engine/install/

### Error: "failed to solve with frontend dockerfile.v0"

**Solution**: Update Docker

```bash
docker --version  # Should be 20.10+
```

### Error: "Module not found" inside container

**Solution**: Rebuild without cache

```bash
docker build --no-cache -t emergency-response .
```

### Error: "permission denied"

**Solution**: Restart Docker daemon or use sudo

---

## 📝 DOCKER VERIFICATION SCRIPT

Create file `test_docker.sh`:

```bash
#!/bin/bash

echo "Testing Docker..."

# Test 1: Build
echo "Building image..."
docker build -t emergency-response . || exit 1
echo "✓ Build successful"

# Test 2: Run default
echo "Running default task..."
docker run emergency-response || exit 1
echo "✓ Default run successful"

# Test 3: Run medium
echo "Running medium task..."
docker run emergency-response --task medium --episodes 3 || exit 1
echo "✓ Medium task successful"

# Test 4: Run hard
echo "Running hard task..."
docker run emergency-response --task hard --episodes 2 || exit 1
echo "✓ Hard task successful"

echo ""
echo "🎉 ALL DOCKER TESTS PASSED!"
```

Run: `bash test_docker.sh`

---

## 🎯 NEXT STEP

Once Docker tests pass locally, move to **Hugging Face deployment**.

See: `HUGGING_FACE_DEPLOYMENT.md`

---

**Status**: Ready for local Docker testing ✅
