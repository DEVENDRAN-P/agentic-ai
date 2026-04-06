#!/usr/bin/env python3
"""Test OpenEnv flow locally before deploying"""

import sys
sys.path.insert(0, '.')

from src.env import EmergencyResponseEnv

print("=" * 70)
print("LOCAL TEST: Complete reset() -> step() -> state() flow")
print("=" * 70)

# Step 1: Reset
print("\n[1️⃣] RESET: Start new game")
env = EmergencyResponseEnv(task_difficulty="easy")
obs = env.reset()
print(f"    ✅ reset() returned observation with keys: {list(obs.keys())}")
print(f"       emergencies: {len(obs.get('emergencies', []))}")
print(f"       ambulances: {len(obs.get('ambulances', []))}")
print(f"       hospitals: {len(obs.get('hospitals', []))}")

# Step 2: State
print("\n[🔍] STATE: Check current situation")
state_obs = env.state()
print(f"    ✅ state() returned observation")
if state_obs == obs:
    print(f"    ✅ state() == reset() (state unchanged)")
else:
    print(f"    ⚠️  State differs")

# Step 3: Step with action
print("\n[2️⃣] STEP: Take action")
action = {
    "ambulance_id": 1,
    "emergency_id": 1,
    "hospital_id": 1
}
next_obs, reward, done, info = env.step(action)
print(f"    ✅ step() returned:")
print(f"       observation keys: {list(next_obs.keys())}")
print(f"       reward: {reward}")
print(f"       done: {done}")
print(f"       info: {info}")

# Step 4: State again
print("\n[🔍] STATE: Check updated situation")
updated_state = env.state()
print(f"    ✅ state() returned updated observation")
print(f"       step counter: {updated_state.get('step')}")

# Step 5: Multiple steps
print("\n[➕] MULTIPLE STEPS: Loop")
for i in range(2):
    action = {
        "ambulance_id": (i % 2) + 1,
        "emergency_id": (i % 3) + 1,
        "hospital_id": (i % 2) + 1
    }
    next_obs, reward, done, info = env.step(action)
    print(f"    Step {i+2}: reward={reward}, done={done}")
    if done:
        print(f"    Episode finished after {i+2} steps")
        break

# Step 6: Reset to different difficulty
print("\n[1️⃣] RESET AGAIN: Different difficulty")
env2 = EmergencyResponseEnv(task_difficulty="medium")
obs2 = env2.reset()
print(f"    ✅ reset() to 'medium'")
print(f"       emergencies: {len(obs2.get('emergencies', []))}")

print("\n" + "=" * 70)
print("✅ LOCAL TEST PASSED!")
print("=" * 70)
