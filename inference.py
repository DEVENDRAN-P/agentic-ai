#!/usr/bin/env python3
"""
OpenEnv Round 1 - Emergency Response Environment Inference Script

MANDATORY LOG FORMAT:
  [START] task=<task_name> env=<env_name> model=<model_name>
  [STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
  [END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn>
"""

import os
import sys
from typing import Optional, List, Tuple, Dict, Any
from src.env import EmergencyResponseEnv
from src.advanced_agents import PriorityHeuristicAgent, ResourceOptimizationAgent, AdaptiveAgent

# Mandatory environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")
TASK_NAME = os.getenv("TASK_NAME", "easy")

def log_start(task: str, env: str, model: str) -> None:
    """Emit mandatory [START] log"""
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    """Emit mandatory [STEP] log - EXACT FORMAT REQUIRED"""
    error_val = error if error else "null"
    done_val = str(done).lower()
    reward_fmt = f"{reward:.2f}"
    print(f"[STEP] step={step} action={action} reward={reward_fmt} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    """Emit mandatory [END] log - EXACT FORMAT REQUIRED"""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    success_val = str(success).lower()
    print(f"[END] success={success_val} steps={steps} rewards={rewards_str}", flush=True)

def run_inference(task_name: str = "easy", max_episodes: int = 5, max_steps_per_episode: int = 30) -> None:
    """
    Run inference with mandatory logging format compatible with OpenEnv Round 1 grading.
    
    Args:
        task_name: One of 'easy', 'medium', 'hard'
        max_episodes: Number of episodes to run
        max_steps_per_episode: Max steps per episode
    """
    
    env_name = "emergency-response-env"
    all_rewards: List[float] = []
    total_steps = 0
    success = True
    
    try:
        # Initialize environment
        env = EmergencyResponseEnv(task_difficulty=task_name)
        log_start(task=task_name, env=env_name, model=MODEL_NAME)
        
        # Select agent based on task difficulty
        if task_name == "easy":
            agent = PriorityHeuristicAgent(env)
        elif task_name == "medium":
            agent = ResourceOptimizationAgent(env)
        else:  # hard
            agent = AdaptiveLearningAgent(env)
        
        # Run multiple episodes
        for episode in range(max_episodes):
            obs = env.reset()
            info = {}  # Empty info dict for first step
            done = False
            
            for step in range(max_steps_per_episode):
                if done:
                    break
                
                total_steps += 1
                
                # Get action from agent
                try:
                    action = agent.get_action(obs)
                except Exception as e:
                    log_step(
                        step=total_steps,
                        action="error",
                        reward=0.0,
                        done=True,
                        error=str(e)[:100]
                    )
                    success = False
                    break
                
                # Execute step in environment
                obs, reward, done, info = env.step(action)
                all_rewards.append(float(reward))
                
                # Format action for logging
                if isinstance(action, (tuple, list)) and len(action) >= 3:
                    action_str = f"assign(ambulance={action[0]}, emergency={action[1]}, hospital={action[2]})"
                else:
                    action_str = str(action)
                
                # Log step
                log_step(
                    step=total_steps,
                    action=action_str,
                    reward=float(reward),
                    done=done,
                    error=None
                )
        
        # Log final result
        log_end(success=success, steps=total_steps, rewards=all_rewards)
        
    except Exception as e:
        # Still emit [END] on error (mandatory)
        log_end(success=False, steps=total_steps, rewards=all_rewards)
        import traceback
        traceback.print_exc(file=sys.stderr)
        print(f"ERROR: {str(e)[:200]}", file=sys.stderr, flush=True)
        sys.exit(1)
    finally:
        if 'env' in locals():
            try:
                if hasattr(env, 'close'):
                    env.close()
            except:
                pass

def main():
    """Main entry point"""
    # Get task from environment variable or default to easy
    task = os.getenv("TASK_NAME", "easy").lower()
    
    # Validate task name
    if task not in ["easy", "medium", "hard"]:
        print(f"ERROR: Invalid task '{task}'. Must be one of: easy, medium, hard", file=sys.stderr)
        sys.exit(1)
    
    # Run inference
    run_inference(task_name=task, max_episodes=5, max_steps_per_episode=30)

if __name__ == "__main__":
    main()
