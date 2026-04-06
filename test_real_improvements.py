#!/usr/bin/env python3
"""
Test Real Improvements: Memory-based selection + Reward threshold strategy

This test shows the impact of the two real improvements:
1. Memory-based action selection (state_hash -> best_action)
2. Reward threshold strategy (only use actions with proven reward)

Expected results:
- More consistent high rewards early in episode
- Fewer zero-reward moves (agent learns to avoid them within episode)
- Higher average score across tasks
"""

import subprocess
import re
import json
from typing import Tuple, List, Dict

def parse_end_log(output: str) -> Dict:
    """Extract [END] log from output"""
    match = re.search(r'\[END\].*?score=([\d.]+)\s+rewards=([\d.,\s]+)', output)
    if not match:
        return None
    
    score = float(match.group(1))
    rewards_str = match.group(2)
    rewards = [float(r.strip()) for r in rewards_str.split(',')]
    
    return {
        "score": score,
        "rewards": rewards,
        "num_rewards": len(rewards),
        "zero_count": sum(1 for r in rewards if r == 0.0),
        "avg_zero_rate": sum(1 for r in rewards if r == 0.0) / len(rewards) if rewards else 0,
        "first_3_avg": sum(rewards[:3]) / 3 if len(rewards) >= 3 else sum(rewards) / len(rewards),
    }

def run_task(task: str, episodes: int = 3) -> List[Dict]:
    """Run inference and collect scores"""
    cmd = f'python inference.py --task {task} --episodes {episodes} --agent heuristic 2>&1'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        
        # Extract all [END] lines
        results = []
        for line in output.split('\n'):
            if '[END]' in line:
                parsed = parse_end_log(line)
                if parsed:
                    results.append(parsed)
        
        return results
    except Exception as e:
        print(f"Error running {task}: {e}")
        return []

def print_analysis(task: str, results: List[Dict]):
    """Print analysis of results"""
    if not results:
        print(f"No results for {task}")
        return
    
    scores = [r["score"] for r in results]
    zero_rates = [r["avg_zero_rate"] for r in results]
    first_3_avgs = [r["first_3_avg"] for r in results]
    
    print(f"\n{'='*60}")
    print(f"TASK: {task.upper()}")
    print(f"{'='*60}")
    print(f"Episodes: {len(results)}")
    print(f"\nScores:")
    print(f"  Episodes: {[f'{s:.2f}' for s in scores]}")
    print(f"  Mean: {sum(scores)/len(scores):.3f}")
    print(f"  Min:  {min(scores):.3f}")
    print(f"  Max:  {max(scores):.3f}")
    
    print(f"\nZero-Reward Percentage (of total rewards):")
    print(f"  Episodes: {[f'{z:.1%}' for z in zero_rates]}")
    print(f"  Mean: {sum(zero_rates)/len(zero_rates):.1%}")
    
    print(f"\nFirst 3 Steps Average Reward:")
    print(f"  Episodes: {[f'{f:.2f}' for f in first_3_avgs]}")
    print(f"  Mean: {sum(first_3_avgs)/len(first_3_avgs):.3f}")
    
    print(f"\nInterpretation:")
    print(f"  - Lower zero% = Better agent decision-making ✓")
    print(f"  - Higher first_3_avg = Agent learns quickly ✓")
    print(f"  - Consistent scores = Reliable agent ✓")
    
    if sum(zero_rates)/len(zero_rates) < 0.70:
        print(f"  ✅ Agent is making meaningful decisions (< 70% zeros)")
    else:
        print(f"  ⚠️  Still too many zeros - agent learning more slowly")

if __name__ == "__main__":
    print("\n👉 TESTING REAL IMPROVEMENTS")
    print("Memory-based selection + Reward threshold strategy\n")
    
    # Test all difficulties
    for task in ["easy", "medium", "hard"]:
        results = run_task(task, episodes=3)
        print_analysis(task, results)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("✅ Improvements implemented:")
    print("  1. Memory-based state-action selection (state_hash -> best_action)")
    print("  2. Reward threshold strategy (only use actions with proven reward)")
    print("  3. Reduced exploration rate (0.15 hard, 0.08 medium/easy)")
    print("\n📊 Monitor these metrics:")
    print("  - Zero-reward %: Should decrease as agent learns")
    print("  - First 3 steps avg: Shows early learning speed")
    print("  - Overall score: Should be stable or improving")
