#!/usr/bin/env python
"""Test active bad action avoidance"""

from src.inference import run_inference

print("\n" + "="*70)
print("TESTING IMPROVED AGENT (Active Bad Action Avoidance)")
print("="*70 + "\n")

# Test with debug mode on to see agent behavior
results = run_inference(
    task_difficulty='hard',
    num_episodes=1,
    agent_type='heuristic',
    verbose=True,
    use_open_env_format=False
)

ep = results['episodes'][0]
print(f"\n{'='*70}")
print(f"Episode Results:")
print(f"  Score: {ep['metrics']['final_score']:.3f}")
print(f"  Reward: {ep['total_reward']:.3f}")
print(f"  Steps: {ep['steps']}")
print(f"  Success: {ep.get('success', False)}")
print(f"{'='*70}")

print("\n📊 Expected Improvements:")
print("  ✓ Fewer repeated bad actions")
print("  ✓ Quicker escape from penalty states")
print("  ✓ Higher scores (>0.7)")
print("  ✓ Agent actively avoiding bad combinations")
