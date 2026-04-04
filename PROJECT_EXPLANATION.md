# 🚨 Emergency Response Environment - Complete Explanation

## 📋 Quick Overview

This is an **AI training environment** that simulates emergency dispatch systems. It's like a video game where an AI learns to:

1. **Assign ambulances** to emergencies
2. **Select hospitals** to send patients
3. **Maximize lives saved** while minimizing response time

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│     AI Agent (LLM/RL/Heuristic)         │
│  Makes decisions: "Assign ambulance X   │
│   to emergency Y at hospital Z"         │
└────────────┬────────────────────────────┘
             │ passes ACTION
             ▼
┌─────────────────────────────────────────┐
│    EmergencyResponseEnv (env.py)        │
│  - Receives action                      │
│  - Updates world state                  │
│  - Calculates reward                    │
│  - Returns new state                    │
└────────────┬────────────────────────────┘
             │ returns STATE
             ▼
┌─────────────────────────────────────────┐
│    Metrics/Grader (graders.py)          │
│  - Scores agent performance             │
│  - Calculates final score [0, 1]        │
└─────────────────────────────────────────┘
```

---

## 📊 How It Works - Step by Step

### **Step 1: Environment Resets**

```python
env = EmergencyResponseEnv("easy")
state = env.reset()
```

**What happens:**

- Creates 3 emergencies (easy mode) with random severity (1-10)
- Places 6 ambulances at random locations
- Sets up 3 hospitals with capacity
- Returns current "state" (what agent observes)

**State example:**

```python
{
  "emergencies": [
    {"id": 1, "severity": 9, "location": 2, "time_waiting": 0, "assigned": False},
    {"id": 2, "severity": 5, "location": 5, "time_waiting": 0, "assigned": False},
    {"id": 3, "severity": 8, "location": 7, "time_waiting": 0, "assigned": False}
  ],
  "ambulances": [
    {"id": 1, "location": 1, "available": True, "busy_until": 0},
    {"id": 2, "location": 4, "available": True, "busy_until": 0},
    ...
  ],
  "hospitals": [
    {"id": 1, "location": 3, "capacity": 10, "patients": 0},
    {"id": 2, "location": 8, "capacity": 10, "patients": 0},
    ...
  ],
  "traffic_level": 2
}
```

**What agent sees:**

- All emergencies with severity levels
- Which ambulances are available NOW
- How much capacity each hospital has

---

### **Step 2: Agent Makes Decision**

The agent looks at state and decides: _"Send ambulance #1 to emergency #3 via hospital #2"_

```python
action = {
    "ambulance_id": 1,      # Which ambulance
    "emergency_id": 3,      # Which emergency to respond to
    "hospital_id": 2        # Where to take the patient
}
```

**Types of agents:**

- **Random**: Pick any valid option randomly
- **Heuristic**: Use rules like "handle high-severity first"
- **LLM**: Ask ChatGPT/Claude what to do
- **RL**: Learned neural network policy

---

### **Step 3: Environment Processes Action**

```python
next_state, reward, done, info = env.step(action)
```

**Inside env.step():**

```python
def step(self, action):
    # 1. Verify action is valid
    if ambulance not available:
        return (state, 0.0, False, {"error": "ambulance busy"})

    # 2. Update ambulance status
    ambulance.available = False  # Mark as busy
    ambulance.busy_until = current_time + travel_time

    # 3. Update emergency status
    emergency.assigned = True
    emergency.assigned_ambulance = ambulance_id

    # 4. Calculate REWARD (the score for this action)
    reward = calculate_reward(state, action, next_state)

    # 5. Return everything
    return (next_state, reward, done, info)
```

---

### **Step 4: Calculate Reward**

The reward function has **3 components**:

```
TOTAL REWARD = 0.5*priority + 0.3*speed + 0.2*resource
```

#### **Component 1: Priority (50% weight)**

```
Did you handle high-severity cases first?

reward_priority = +0.5 if handled severity-8+ case first
                = -0.5 if ignored critical case
                = -0.1 for each step delay on high-severity case
```

**Example:**

- Emergency with severity 9 waiting long? → BIG PENALTY
- Emergency with severity 3? → Can wait longer

#### **Component 2: Response Speed (30% weight)**

```
How fast did ambulance reach the emergency?

travel_time = distance(ambulance, emergency) * traffic_factor

reward_speed = +0.3 if fast (travel_time < 3 steps)
             = +0.0 if medium (travel_time = 3-5)
             = -0.3 if slow (travel_time > 5)
```

**Example:**

- Ambulance 1 step away = +0.3 reward ✓
- Ambulance 8 steps away = -0.3 reward ✗

#### **Component 3: Resource Usage (20% weight)**

```
Did you use hospitals efficiently?

reward_resource = +0.2 if sent to hospital with capacity
                = -0.1 if hospital was full (bounced patient)
                = 0.0 if neutral
```

**Example:**

- Hospital 1 is full (0 capacity): Don't send there → +0.2
- Hospital 2 has 5 beds: Send there → +0.2

---

## 📁 Project Structure Explained

### **File: `src/env.py` (The Simulation)**

This is the **heart** of the system. It simulates the entire emergency response world.

**Key class: `EmergencyResponseEnv`**

```python
class EmergencyResponseEnv:
    def __init__(self, task_difficulty="easy"):
        # Set parameters based on difficulty
        if difficulty == "easy":
            self.num_emergencies = 3
            self.num_ambulances = 6
            self.traffic_factor = 1.0  # No traffic

        elif difficulty == "medium":
            self.num_emergencies = 5
            self.num_ambulances = 6
            self.traffic_factor = 1.5  # Some traffic

        else:  # hard
            self.num_emergencies = 8
            self.num_ambulances = 6
            self.traffic_factor = 2.0  # Heavy traffic

    def reset(self):
        """Create new scenario, return initial state"""
        # Spawn emergencies randomly
        # Place ambulances randomly
        # Initialize hospitals
        # Return state

    def step(self, action):
        """Process one action"""
        # Update world state
        # Calculate reward
        # Return (state, reward, done, info)
```

**What env.py tracks:**

- Emergency IDs, locations, severities, wait times
- Ambulance availability and locations
- Hospital capacities
- Traffic levels
- Overall metrics (lives saved, response time)

---

### **File: `src/graders.py` (The Scoring System)**

Calculates the final score after an episode completes.

```python
def evaluate_episode(env, step_history):
    """
    After 100 steps, calculate how well the agent did.
    """
    stats = {
        "priority_handling": calculate_priority(env, step_history),
        "response_speed": calculate_speed(env, step_history),
        "resource_usage": calculate_resource(env, step_history),
    }

    # Weighted average
    final_score = (
        0.5 * stats["priority_handling"] +
        0.3 * stats["response_speed"] +
        0.2 * stats["resource_usage"]
    )

    # Normalize to [0.0, 1.0]
    return clamp(final_score, 0.0, 1.0)
```

**Output example:**

```
{
  "priority_handling": 0.85,      # 85% - Good on high-severity
  "response_speed": 0.70,          # 70% - Medium speed
  "resource_usage": 0.90,          # 90% - Good efficiency
  "final_score": 0.82              # Overall: 82/100
}
```

---

### **File: `src/inference.py` (Agent Interaction)**

Shows how agents interact with the environment.

```python
class RandomBaselineAgent:
    """Simple test agent - picks random valid actions"""
    def get_action(self, state):
        available_ambulances = [a for a in state["ambulances"] if a["available"]]
        unassigned_emergencies = [e for e in state["emergencies"] if not e["assigned"]]
        available_hospitals = [h for h in state["hospitals"] if h["capacity"] > 0]

        # Pick randomly from available options
        action = {
            "ambulance_id": random.choice(available_ambulances).id,
            "emergency_id": random.choice(unassigned_emergencies).id,
            "hospital_id": random.choice(available_hospitals).id
        }
        return action

class SmartHeuristicAgent:
    """Smart test agent - follows rules"""
    def get_action(self, state):
        # Rule 1: Handle highest severity first
        target_emergency = max(
            [e for e in state["emergencies"] if not e["assigned"]],
            key=lambda e: e["severity"]
        )

        # Rule 2: Use closest ambulance
        available_ambulances = [a for a in state["ambulances"] if a["available"]]
        closest_ambulance = min(
            available_ambulances,
            key=lambda a: abs(a["location"] - target_emergency["location"])
        )

        # Rule 3: Use hospital with most capacity
        available_hospitals = [h for h in state["hospitals"] if h["capacity"] > 0]
        best_hospital = max(available_hospitals, key=lambda h: h["capacity"])

        return {
            "ambulance_id": closest_ambulance.id,
            "emergency_id": target_emergency.id,
            "hospital_id": best_hospital.id
        }

def run_episode(env, agent):
    """Run one complete episode"""
    state = env.reset()
    total_reward = 0.0

    for step in range(100):
        # Get action from agent
        action = agent.get_action(state)

        # Environment processes action
        next_state, reward, done, info = env.step(action)

        total_reward += reward

        print(f"[STEP] step={step} action={action} reward={reward:.3f}")

        state = next_state
        if done:
            break

    return total_reward
```

---

### **File: `src/advanced_agents.py` (Sophisticated Agents)**

Different agent strategies:

```python
class PriorityHeuristicAgent:
    """Multi-factor scoring"""
    def get_action(self, state):
        # Score each emergency: 0.7*severity + 0.3*waiting_time
        scored_emergencies = [
            (0.7*e["severity"] + 0.3*e["time_waiting"], e)
            for e in state["emergencies"]
        ]
        target = max(scored_emergencies)[1]  # Pick highest score

        # Advanced hospital selection
        best_hospital = None
        best_score = -float('inf')
        for h in state["hospitals"]:
            # Balance capacity + proximity
            score = 0.6*h["capacity"] + 0.4*(10 - distance(h, target))
            if score > best_score:
                best_score = score
                best_hospital = h

        return {"ambulance_id": ..., "emergency_id": ..., "hospital_id": ...}

class ResourceOptimizationAgent:
    """Focus on even distribution"""
    def get_action(self, state):
        # Load balance across hospitals
        # Rotate ambulances fairly
        # Minimize idle time
        ...

class AdaptiveAgent:
    """Learns from history"""
    def __init__(self):
        self.episode_memory = []

    def get_action(self, state):
        # Learn what worked well before
        # Repeat successful patterns
        ...

class EnsembleAgent:
    """Voting from multiple strategies"""
    def get_action(self, state):
        # Get votes from multiple agents
        # Return majority decision
        ...

class LLMReadyAgent:
    """Ready for ChatGPT/Claude integration"""
    def get_action(self, state):
        prompt = f"""
        Current state: {json.dumps(state)}

        What's the best action? Return JSON:
        {{"ambulance_id": ..., "emergency_id": ..., "hospital_id": ...}}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content)
```

---

## 🎮 Complete Example Walkthrough

```
EPISODE START
─────────────────────────────────────────

Initial State (after reset):
┌─────────────────────────────────────────────────┐
│ EMERGENCIES:                                    │
│  • ID 1: severity=9 (CRITICAL!), location=2    │
│  • ID 2: severity=5 (mild), location=5         │
│  • ID 3: severity=8 (HIGH), location=7         │
├─────────────────────────────────────────────────┤
│ AMBULANCES:                                     │
│  • ID 1: location=1, AVAILABLE ✓                │
│  • ID 2: location=4, AVAILABLE ✓                │
│  • ID 3-6: ..., AVAILABLE ✓                     │
├─────────────────────────────────────────────────┤
│ HOSPITALS:                                      │
│  • ID 1: location=3, capacity=10/10, patients=0│
│  • ID 2: location=8, capacity=10/10, patients=0│
│  • ID 3: location=5, capacity=10/10, patients=0│
└─────────────────────────────────────────────────┘

─────────────────────────────────────────

STEP 1:
Agent sees: State above
Agent thinks: "Emergency #1 is CRITICAL (severity 9)!
              Send closest ambulance there!"

Agent action:
{
    "ambulance_id": 1,      # Closest ambulance (distance = 1)
    "emergency_id": 1,      # Target: critical emergency
    "hospital_id": 1        # Closest hospital
}

Environment processes:
  ✓ Ambulance 1 is available
  ✓ Emergency 1 unassigned
  ✓ Hospital 1 has capacity

Reward calculation:
  • Priority: +0.5 (handled severity-9 first!)
  • Speed: +0.3 (very close, 1 step)
  • Resource: +0.2 (sent to hospital with capacity)
  TOTAL REWARD = 1.0 ✅ PERFECT!

Output:
[STEP] step=1 action=(1,1,1) reward=1.000

State update:
  • Ambulance 1: available=False, busy_until=5
  • Emergency 1: assigned=True, assigned_ambulance=1
  • Hospital 1: patients=1, capacity=9

─────────────────────────────────────────

STEP 2:
Agent sees: Updated state
  Emergency 1 is now handled (assigned)
  Emergency 3 (severity=8) now most critical
  Ambulance 2-6 available, Ambulance 1 busy

Agent action: Assign ambulance 2 to emergency 3
{
    "ambulance_id": 2,
    "emergency_id": 3,
    "hospital_id": 2
}

Reward calculation:
  • Priority: +0.5 (handled second-highest severity)
  • Speed: +0.1 (medium distance, takes ~3 steps)
  • Resource: +0.2
  TOTAL REWARD = 0.8 ✅ Good!

Output:
[STEP] step=2 action=(2,3,2) reward=0.800

State update:
  • Ambulance 2: available=False, busy_until=8
  • Emergency 3: assigned=True
  • Hospital 2: patients=1, capacity=9

─────────────────────────────────────────

... more steps ...

─────────────────────────────────────────

EPISODE END (after 100 steps or all emergencies handled)

Episode Summary:
  • Total steps: 47
  • Total reward: 32.5
  • Emergencies handled: 3/3
  • High-severity handled first: YES
  • Average response time: 3.2 steps

Grader output:
  • Priority handling score: 0.95 (excellent)
  • Response speed score: 0.85 (good)
  • Resource usage score: 0.88 (good)
  • FINAL SCORE: 0.89 (89/100) ⭐ Excellent!

[END] success=true steps=47 avg_score=0.89
```

---

## 🎯 Task Difficulties Explained

### **EASY 🟢**

- 3 emergencies
- 6 ambulances (all available)
- 3 hospitals (10 bed capacity each)
- No traffic (1.0x speed)
- **Goal**: Basic assignment works

### **MEDIUM 🟡**

- 5 emergencies
- 6 ambulances (2 busy initially)
- 3 hospitals (4 bed capacity each)
- Moderate traffic (1.5x slower)
- **Goal**: Prioritization under constraints

### **HARD 🔴**

- 8 emergencies
- 6 ambulances (4 busy initially)
- 3 hospitals (2 bed capacity each)
- Heavy traffic (2.0x slower)
- **Goal**: Complex decision-making

---

## 🔄 Data Flow Diagram

```
┌──────────────────────────┐
│  AI Agent                │ ← Receives state
│  (Random/Heuristic/LLM)  │
└──────────────┬───────────┘
               │ action: {ambulance_id, emergency_id, hospital_id}
               ▼
┌──────────────────────────────────────────┐
│  EmergencyResponseEnv.step(action)       │
│                                          │
│  1. Validate action                      │
│     ├─ ambulance available? ✓            │
│     ├─ emergency unassigned? ✓           │
│     └─ hospital has capacity? ✓          │
│                                          │
│  2. Update internal state                │
│     ├─ Mark ambulance busy               │
│     ├─ Mark emergency assigned           │
│     └─ Reduce hospital capacity          │
│                                          │
│  3. Calculate reward                     │
│     ├─ Priority component (0.5 weight)   │
│     ├─ Speed component (0.3 weight)      │
│     └─ Resource component (0.2 weight)   │
│     = TOTAL REWARD ∈ [0.0, 1.0]          │
│                                          │
│  4. Return new state                     │
└──────────────┬───────────────────────────┘
               │ (state, reward, done, info)
               ▼
┌──────────────────────────┐
│  Agent observes new state│
│  and prepares next action│
└──────────────────────────┘
```

---

## 📊 Example Output Format

```
[START] task=easy env=emergency-response-env model=heuristic episodes=5

[STEP] episode=1 step=1 action=(1,2,3) reward=0.950
[STEP] episode=1 step=2 action=(3,1,2) reward=0.650
[STEP] episode=1 step=3 action=(2,3,1) reward=0.600
...
[STEP] episode=1 step=15 action=(5,2,2) reward=0.850
[END-EPISODE] episode=1 total_reward=12.50

[STEP] episode=2 step=1 action=(2,1,1) reward=0.900
...

[END] success=true episodes=5 avg_score=1.000
      rewards=2.58,2.60,2.55,2.43,2.05
```

---

## 🧠 Key Concepts

| Concept        | Meaning                                                   |
| -------------- | --------------------------------------------------------- |
| **State**      | What agent observes (emergencies, ambulances, hospitals)  |
| **Action**     | What agent decides (which ambulance, emergency, hospital) |
| **Reward**     | How good the action was (0.0 = bad, 1.0 = excellent)      |
| **Episode**    | One complete run until all emergencies handled            |
| **Step**       | One single action in an episode                           |
| **Difficulty** | How hard the scenario is (easy/medium/hard)               |
| **Grader**     | System that scores final performance                      |
| **Agent**      | The AI making decisions                                   |

---

## 🚀 How to Use

**Run validation (check everything works):**

```bash
python validate_hackathon.py
```

**Run tests:**

```bash
python tests/test_env.py
```

**Run inference with basic heuristic:**

```bash
python inference.py --task easy --episodes 5 --agent heuristic
```

**Run with environment variable:**

```bash
$env:TASK_NAME = "hard"; python inference.py
```

---

This is the complete system! The agent learns to solve emergency dispatch problems by receiving feedback (rewards) and improving its decisions over time.
