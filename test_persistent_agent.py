#!/usr/bin/env python
"""Test agent with persistent bad-action learning across episodes (like real inference)"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

print("\n" + "="*70)
print("TESTING PERSISTENT AGENT - 5 EPISODES (LIKE REAL INFERENCE)")
print("="*70 + "\n")

# CRITICAL: Create ONE agent that persists across episodes
env = EmergencyResponseEnv(task_difficulty='hard')
agent = SmartHeuristicAgent(env, debug=False)

results = []

for ep_num in range(5):
    env = EmergencyResponseEnv(task_difficulty='hard')  # Fresh env each episode
    state = env.reset()
    
    actions_sequence = []
    repeated_bad_count = 0
    
    done = False
    step = 0
    while not done and step < 30:
        action = agent.get_action(state)
        action_tuple = (action["ambulance_id"], action["emergency_id"], action["hospital_id"])
        
        next_state, reward, done, info = env.step(action)
        
        # Agent learns about bad actions
        if reward <= -0.30:
            agent.mark_action_bad(action, reward)
        
        actions_sequence.append((action_tuple, reward))
        
        # Count repeated bad actions within THIS episode  
        if step > 0 and reward <= -0.40:
            recent_bad = [(a, r) for a, r in actions_sequence[max(0, step-5):step] if r <= -0.40 and a == action_tuple]
            if recent_bad:
                repeated_bad_count += 1
                print(f"  ⚠️  EP{ep_num+1} REPEAT: {action_tuple} → {reward:.2f} (first seen at step {max(0, step-5)}-{step})")
        
        step += 1
        state = next_state
    
    bad_count = sum(1 for _, r in actions_sequence if r <= -0.40)
    good_count = sum(1 for _, r in actions_sequence if r > 0)
    score = sum(r for _, r in actions_sequence)
    
    results.append({
        'episode': ep_num + 1,
        'score': score,
        'steps': len(actions_sequence),
        'bad': bad_count,
        'good': good_count,
        'repeated': repeated_bad_count
    })
    
    print(f"Episode {ep_num+1}: Score={score:+.3f}, Steps={len(actions_sequence):2d}, Repeated-Bad={repeated_bad_count}, Bad={bad_count}, Good={good_count}")

print("\n" + "="*70)
print("SUMMARY (PERSISTENT AGENT)")
print("="*70)

avg_score = sum(r['score'] for r in results) / len(results)
avg_repeated = sum(r['repeated'] for r in results) / len(results)
avg_steps = sum(r['steps'] for r in results) / len(results)
total_repeated = sum(r['repeated'] for r in results)

print(f"Average Score: {avg_score:+.3f}")
print(f"Average Repeated Bad Actions: {avg_repeated:.1f}")
print(f"Total Repeated Bad Actions (across 5 episodes): {total_repeated}")
print(f"Average Steps: {avg_steps:.1f}")

if avg_repeated == 0:
    print("\n✅ SUCCESS: No repeated bad actions across all episodes!")
    print("   Agent is learning and remembering bad actions!")
else:
    print(f"\n⚠️  {total_repeated} repeated bad actions detected")
    print("   Agent is NOT fully learning to avoid repeated failures")
    
print("="*70)
