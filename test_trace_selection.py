#!/usr/bin/env python
"""Trace how actions are selected and whether bad-action checking is used"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

env = EmergencyResponseEnv(task_difficulty='hard')
agent = SmartHeuristicAgent(env, debug=True)  # Enable debug mode

state = env.reset()

print("\n" + "="*70)
print("TRACING ACTION SELECTION - First 10 steps")
print("="*70)

for step in range(10):
    print(f"\n[STEP {step+1}]")
    print(f"  Bad actions known: {len(agent.bad_action_penalties)}")
    if agent.bad_action_penalties:
        print(f"  Bad action penalties: {dict(list(agent.bad_action_penalties.items())[:5])}")
    
    action = agent.get_action(state)
    action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
    
    next_state, reward, done, info = env.step(action)
    
    is_bad = agent.is_action_bad(action_tuple[0], action_tuple[1], action_tuple[2])
    print(f"  Selected: {action_tuple}, Reward: {reward:+.2f}, Is-Bad: {is_bad}")
    
    if reward <= -0.30:
        agent.mark_action_bad(action, reward)
        print(f"  >>> MARKED AS BAD")
    
    state = next_state
    if done:
        break

print("\n" + "="*70)
