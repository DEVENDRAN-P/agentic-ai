#!/usr/bin/env python
"""Debug success field tracking"""

from src.inference import run_inference

results = run_inference(task_difficulty='medium', num_episodes=2, agent_type='heuristic', verbose=False)

print("\n" + "="*60)
print("SUCCESS FIELD DEBUG")
print("="*60)

for ep in results['episodes']:
    success_val = ep.get('success', 'NOT FOUND')
    score = ep['metrics']['final_score']
    print(f"\nEpisode {ep['episode']}:")
    print(f"  Score: {score:.3f}")
    print(f"  Success field: {success_val}")
    print(f"  Type: {type(success_val)}")
    print(f"  Condition (score > 0.5): {score > 0.5}")
    print(f"  Bool(success): {bool(success_val)}")
    
print("\n" + "="*60)
print(f"Total successful: {sum(1 for ep in results['episodes'] if ep.get('success'))}")
print(f"Total episodes: {len(results['episodes'])}")
