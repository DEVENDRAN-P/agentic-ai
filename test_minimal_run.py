#!/usr/bin/env python
"""Minimal test mimicking run_inference to trace repeated bad actions"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

print("\n" + "="*70)
print("MINIMAL RUN_INFERENCE SIMULATION")
print("="*70)

# Create agent ONCE (like run_inference does at line 595)
env_temp = EmergencyResponseEnv(task_difficulty='hard', seed=42)
agent = SmartHeuristicAgent(env_temp, debug=False)

print(f"\nAgent created: SmartHeuristicAgent")
print(f"  is_action_bad method: {hasattr(agent, 'is_action_bad')}")
print(f"  mark_action_bad method: {hasattr(agent, 'mark_action_bad')}")

# Now run episode 1
print("\n" + "-"*70)
print("EPISODE 1 (seed=42)")
print("-"*70)

env = EmergencyResponseEnv(task_difficulty='hard', seed=42)
state = env.reset()

episode_step = 0
repeated_bad_count = 0

while episode_step < 30:
    # Get action
    action = agent.get_action(state)
    action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
    
    # Step environment
    next_state, reward, done, info = env.step(action)
    
    # Check if already bad
    is_bad_before = agent.is_action_bad(action_tuple[0], action_tuple[1], action_tuple[2])
    
    # Mark as bad if applicable
    if hasattr(agent, 'mark_action_bad') and reward <= -0.30:
        agent.mark_action_bad(action, reward)
    
    # Check if bad after (should still be True if already bad)
    is_bad_after = agent.is_action_bad(action_tuple[0], action_tuple[1], action_tuple[2])
    
    # Print with indicators
    bad_marker = ""
    if is_bad_before:
        bad_marker = " ⚠️  [WAS ALREADY MARKED BAD!]"
        repeated_bad_count += 1
    elif reward <= -0.30:
        bad_marker = " [MARKED BAD]"
    
    print(f"Step {episode_step+1:2d}: {action_tuple} → {reward:+.2f}{bad_marker}")
    
    episode_step += 1
    state = next_state
    
    if done:
        break

print(f"\n⚠️  Repeated bad actions (selected when already marked bad): {repeated_bad_count}")
print("="*70)
