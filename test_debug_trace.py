#!/usr/bin/env python
"""Debug trace to see which path selected repeated bad actions"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

print("\n" + "="*70)
print("DEBUG TRACE - Find why bad actions are selected")
print("="*70 + "\n")

agent = SmartHeuristicAgent(EmergencyResponseEnv(task_difficulty='hard'), debug=True)

for ep_num in range(2):
    if ep_num > 0:
        print("\n" + "="*70 + "\n")
    
    env = EmergencyResponseEnv(task_difficulty='hard')
    state = env.reset()
    
    print(f"[EPISODE {ep_num+1}] Starting with {len(agent.bad_action_penalties)} known-bad actions")
    
    actions_sequence = []
    
    done = False
    step = 0
    while not done and step < 30:
        action = agent.get_action(state)
        action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
        
        next_state, reward, done, info = env.step(action)
        
        # Check if this was a known-bad action
        was_bad = agent.is_action_bad(action_tuple[0], action_tuple[1], action_tuple[2])
        penalty_count = agent.bad_action_penalties.get(action_tuple, 0)
        
        if reward <= -0.30:
            agent.mark_action_bad(action, reward)
        
        if was_bad:
            print(f"⚠️  REPEATING BAD ACTION: Step {step+1}, {action_tuple} (penalty_count={penalty_count})")
        
        actions_sequence.append((action_tuple, reward))
        step += 1
        state = next_state
    
    print(f"  Episode {ep_num+1} complete: {len(actions_sequence)} steps")

print("\n" + "="*70)
