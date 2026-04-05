#!/usr/bin/env python
"""Test WITHOUT seed to match inference randomness"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

print("\n" + "="*70)
print("MULTIPLE EPISODES WITHOUT SEED (matches inference randomness)")
print("="*70)

# Create agent ONCE (like run_inference does)
env_temp = EmergencyResponseEnv(task_difficulty='hard')
agent = SmartHeuristicAgent(env_temp, debug=False)

for episode in range(3):
    print(f"\nEpisode {episode+1}:")
    
    env = EmergencyResponseEnv(task_difficulty='hard')  
    state = env.reset()
    
    episode_step = 0
    repeated_bad_count = 0
    episode_actions = []
    
    while episode_step < 30:
        action = agent.get_action(state)
        action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
        
        next_state, reward, done, info = env.step(action)
        
        is_bad_before = agent.is_action_bad(action_tuple[0], action_tuple[1], action_tuple[2])
        
        if hasattr(agent, 'mark_action_bad') and reward <= -0.30:
            agent.mark_action_bad(action, reward)
        
        episode_actions.append((action_tuple, reward, is_bad_before))
        
        if is_bad_before:
            repeated_bad_count += 1
        
        episode_step += 1
        state = next_state
        
        if done:
            break
    
    # Check for repeated bad actions within THIS episode
    step_range = []
    for i, (act, rew, was_bad) in enumerate(episode_actions):
        if i > 0 and rew <= -0.40:
            # Check if same action with bad reward in recent history
            for j in range(max(0, i-5), i):
                if episode_actions[j][0] == act and episode_actions[j][1] <= -0.40:
                    step_range.append(f"{act}:steps({j+1},{i+1})")
    
    print(f"  Steps: {episode_step}, Bad-when-selected: {repeated_bad_count}, Repeated within episode: {len(set(step_range))}")
    if step_range:
        print(f"  Repeats: {', '.join(list(set(step_range))[:5])}")

print("\n" + "="*70)
