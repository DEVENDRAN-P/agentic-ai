#!/usr/bin/env python
"""
ENHANCEMENT TEST: Smarter Agent with Better Repetition Avoidance

Tests the improved heuristic agent that:
1. Tracks 0.00 rewards and avoids repeating them
2. Records good actions for prioritization
3. Smarter exploration that avoids known-bad combinations
"""

import subprocess
import sys

print("=" * 90)
print("TESTING: ENHANCED SMART HEURISTIC AGENT")
print("=" * 90)
print("\nImprovements implemented:")
print("  ✅ Track 0.00 rewards and mark action as bad if repeated")
print("  ✅ Maintain good_actions set for positive reward combinations")
print("  ✅ Record action_rewards history for analysis")
print("  ✅ Track zero_reward_count separately")
print("\nExpected improvement:")
print("  ❌ BEFORE: Repeats (2,1,2) → 0.00, (2,1,2) → 0.00, (2,1,2) → 0.00")
print("  ✅ AFTER: Tries (2,1,2) → 0.00, then avoids it, tries different action")
print("\n" + "=" * 90)
print()

# Run tests
for task in ["easy", "medium", "hard"]:
    print(f"\n🧪 Testing {task.upper()} task with ENHANCED agent...")
    result = subprocess.run([
        sys.executable, "inference.py",
        "--task", task,
        "--episodes", "1",
        "--agent", "heuristic"
    ], capture_output=True, text=True, timeout=30)
    
    output = result.stdout + result.stderr
    
    # Find END line
    end_lines = [line for line in output.split('\n') if '[END]' in line]
    if end_lines:
        end_line = end_lines[0]
        print(f"   {end_line}")
        
        # Extract metrics
        import re
        score_match = re.search(r'score=([0-9.]+)', end_line)
        steps_match = re.search(r'steps=(\d+)', end_line)
        rewards_part = end_line.split("rewards=")[1] if "rewards=" in end_line else ""
        
        if score_match and steps_match:
            score = float(score_match.group(1))
            steps = int(steps_match.group(1))
            print(f"   Score: {score:.3f}, Steps: {steps}")
            
            # Count zeros
            try:
                rewards = [float(r.strip()) for r in rewards_part.split(',') if r.strip()]
                zero_count = sum(1 for r in rewards if r == 0.0)
                print(f"   Zero rewards: {zero_count}/{len(rewards)} - Goal is to reduce this")
            except:
                pass

print("\n" + "=" * 90)
print("ANALYSIS")
print("=" * 90)

print("""
The enhanced agent should show:

1. Smart avoidance of zero-reward actions:
   - When action gets 0.00, agent remembers it
   - If tried again gets 0.00, it's marked as bad
   - Next time, agent avoids this action

2. Better scores on hard task:
   - Should see fewer repeated 0.00 values
   - More exploration of different action combinations
   - Higher number of successful (positive reward) actions

3. Profile:
   Easy:   Should stay perfect (1.00)
   Medium: Same or better (0.95)
   Hard:   Should improve towards 0.85-0.90 range

""")
