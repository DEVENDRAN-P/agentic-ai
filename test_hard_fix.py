#!/usr/bin/env python
"""Quick test for hard task looping fix"""

from src.inference import run_inference

print("=" * 60)
print("Testing Hard Task Looping Fix")
print("=" * 60)

results = run_inference(task_difficulty='hard', num_episodes=2, agent_type='heuristic', verbose=True)

print('\n' + '=' * 60)
print('Test Results:')
print('=' * 60)
for ep in results['episodes']:
    print(f"Episode {ep['episode']}: Score={ep['metrics']['final_score']:.3f}, Reward={ep['total_reward']:.3f}, Steps={ep['steps']}")

print(f"\nAverage Score: {results['statistics']['final_score']['mean']:.3f}")
print(f"Status: {'✅ PASS' if results['statistics']['final_score']['mean'] > 0 else '❌ FAIL'}")
