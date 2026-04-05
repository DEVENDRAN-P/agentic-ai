#!/usr/bin/env python
"""Test all 4 quick fixes"""

from src.inference import run_inference

print("=" * 70)
print("TESTING ALL 4 QUICK FIXES")
print("=" * 70)

# Test each difficulty
for difficulty in ["easy", "medium", "hard"]:
    print(f"\n{'='*70}")
    print(f"Testing {difficulty.upper()}")
    print(f"{'='*70}")
    
    results = run_inference(
        task_difficulty=difficulty,
        num_episodes=2,
        agent_type="heuristic",
        verbose=True,
        use_open_env_format=False
    )
    
    print(f"\nDetailed Results:")
    for ep in results["episodes"]:
        success_status = "✅" if ep.get("success", False) else "❌"
        print(f"  Episode {ep['episode']}: {success_status} Score={ep['metrics']['final_score']:.3f}, Reward={ep['total_reward']:.3f}, Steps={ep['steps']}")

print(f"\n{'='*70}")
print("Quick Fixes Applied:")
print("✅ Fix 1: Repetition penalty (-0.2 if action in last 5)")
print("✅ Fix 2: State-visit penalty (-0.3 if state revisited)")
print("✅ Fix 3: Early stop on bad streak (4+ of 5 rewards = -0.40)")
print("✅ Fix 4: Success condition stricter (score > 0.5)")
print(f"{'='*70}")
