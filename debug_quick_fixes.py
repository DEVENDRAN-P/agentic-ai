#!/usr/bin/env python
"""Debug test for quick fixes"""

from src.inference import SmartHeuristicAgent
from src.env import EmergencyResponseEnv

print("Testing success condition logic...")

# Test with different scores
test_cases = [
    (0.912, False, True),   # score > 0.5, no bad streak → should pass
    (0.878, False, True),   # score > 0.5, no bad streak → should pass
    (0.191, False, False),  # score < 0.5, no bad streak → should fail
    (0.700, False, True),   # score > 0.5, no bad streak → should pass
    (0.912, True, False),   # score > 0.5, BUT bad streak → should fail
]

for score, bad_streak, expected in test_cases:
    # Replicate the success condition
    episode_success = (not bad_streak and score > 0.5)
    result = "✅" if episode_success == expected else "❌"
    print(f"{result} Score={score:.3f}, BadStreak={bad_streak} → Success={episode_success} (expected {expected})")

# Now test a real episode with debugging
print("\n\nTesting a MEDIUM episode with detailed logging:")
env = EmergencyResponseEnv(task_difficulty="medium")
agent = SmartHeuristicAgent(env, debug=False)  # Set to True for detailed trace

state = env.reset()
total_reward = 0.0
step_history = []
bad_streak_detected = False

# Reset tracking
if hasattr(agent, 'last_k_actions'):
    agent.last_k_actions.clear()
if hasattr(agent, 'visited_states'):
    agent.visited_states.clear()

episode_step = 0
done = False
while not done and episode_step < 20:
    action = agent.get_action(state)
    next_state, reward, done, info = env.step(action)
    
    step_history.append((state, action, reward, done))
    total_reward += reward
    episode_step += 1
    
    if hasattr(agent, 'record_reward'):
        agent.record_reward(float(reward))
    
    # Check for bad streak
    if hasattr(agent, 'last_5_rewards') and len(agent.last_5_rewards) >= 5:
        bad_count = sum(1 for r in agent.last_5_rewards if r <= -0.40)
        if bad_count >= 4:
            bad_streak_detected = True
            print(f"[BAD STREAK DETECTED at step {episode_step}]")
            break
    
    state = next_state

# Calculate metrics
from src.graders import create_grader_for_task
grader = create_grader_for_task("medium")
episode_metrics = grader.evaluate_episode(env, step_history)

# Check success
episode_success = (not bad_streak_detected and episode_metrics["final_score"] > 0.5)

print(f"\nEpisode Results:")
print(f"  Steps: {episode_step}")
print(f"  Total Reward: {total_reward:.3f}")
print(f"  Final Score: {episode_metrics['final_score']:.3f}")
print(f"  Bad Streak Detected: {bad_streak_detected}")
print(f"  Success: {episode_success}")
