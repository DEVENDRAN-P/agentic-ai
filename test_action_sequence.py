#!/usr/bin/env python
"""Detailed test showing action sequences"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent
from src.graders import create_grader_for_task

print("\n" + "="*70)
print("DETAILED ACTION SEQUENCE TEST")
print("="*70 + "\n")

env = EmergencyResponseEnv(task_difficulty='hard')
agent = SmartHeuristicAgent(env, debug=False)

state = env.reset()
step_history = []
actions_sequence = []

done = False
step = 0
while not done and step < 30:
    # Get action
    action = agent.get_action(state)
    action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
    
    # Execute
    next_state, reward, done, info = env.step(action)
    
    # Agent learns about bad actions
    if reward <= -0.30:
        agent.mark_action_bad(action, reward)
    
    actions_sequence.append((action_tuple, reward))
    step_history.append((state, action, reward, done))
    
    step += 1
    state = next_state

print("Action Sequence (ambulance, emergency, hospital) → reward:")
print("-" * 70)

# Check for repeated bad actions
repeated_count = 0
for i, (action, reward) in enumerate(actions_sequence):
    if i > 0 and reward <= -0.40:
        # Check if this action appeared recently
        recent_bad = [a for a, r in actions_sequence[max(0, i-5):i] if r <= -0.40 and a == action]
        if recent_bad:
            repeated_count += 1
            marker = " ⚠️ REPEAT BAD"
        else:
            marker = ""
    else:
        marker = ""
    
    print(f"Step {i+1:2d}: {str(action):20s} → {reward:+.2f}{marker}")

print("-" * 70)
print(f"\nStatistics:")
print(f"  Total steps: {len(actions_sequence)}")
print(f"  Repeated bad actions: {repeated_count}")
print(f"  Bad rewards (-0.40): {sum(1 for _, r in actions_sequence if r <= -0.40)}")
print(f"  Good rewards (+): {sum(1 for _, r in actions_sequence if r > 0)}")

# Calculate score
grader = create_grader_for_task('hard')
metrics = grader.evaluate_episode(env, step_history)
print(f"  Final score: {metrics['final_score']:.3f}")

print("\n✅ If repeated bad actions < 3, agent is learning!")
print(f"   Current: {repeated_count} repeated bad actions")
print("="*70)
