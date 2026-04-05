#!/usr/bin/env python
"""Detailed trace of actions in hard task - shows what agent is doing"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

print("\n" + "="*70)
print("DETAILED ACTION TRACE - First 2 episodes")
print("="*70 + "\n")

agent = SmartHeuristicAgent(EmergencyResponseEnv(task_difficulty='hard'), debug=False)

for ep_num in range(2):
    env = EmergencyResponseEnv(task_difficulty='hard')
    state = env.reset()
    
    print(f"[EPISODE {ep_num+1}]")
    actions_sequence = []
    
    done = False
    step = 0
    while not done and step < 30:
        action = agent.get_action(state)
        action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
        
        next_state, reward, done, info = env.step(action)
        
        if reward <= -0.30:
            agent.mark_action_bad(action, reward)
        
        actions_sequence.append((action_tuple, reward))
        
        # Check if bad action is marked
        is_bad = agent.is_action_bad(action_tuple[0], action_tuple[1], action_tuple[2])
        bad_marker = " [MARKED BAD]" if is_bad else ""
        
        # Check for repeats in recent history
        repeat_marker = ""
        if step >= 1 and reward <= -0.40:
            for prev_idx in range(max(0, step-5), step):
                if actions_sequence[prev_idx][0] == action_tuple and actions_sequence[prev_idx][1] <= -0.40:
                    repeat_marker = f" ⚠️ REPEAT (step {prev_idx})"
                    break
        
        print(f"  Step {step+1:2d}: {action_tuple} → {reward:+.2f}{bad_marker}{repeat_marker}")
        
        step += 1
        state = next_state
    
    bad_count = sum(1 for _, r in actions_sequence if r <= -0.40)
    print(f"  Summary: {len(actions_sequence)} steps, {bad_count} bad, Score={sum(r for _, r in actions_sequence):+.2f}")
    print()

print("="*70)
print(f"\nAgent's bad_action_penalties dict after testing:")
print(f"  {len(agent.bad_action_penalties)} unique bad actions learned")
if agent.bad_action_penalties:
    for action, count in sorted(agent.bad_action_penalties.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {action}: {count} failures")
print("="*70)
