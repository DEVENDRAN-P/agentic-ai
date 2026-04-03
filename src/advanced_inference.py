"""
Advanced Inference Script with All Features

Demonstrates how to use all advanced features:
- Multiple agent types
- Performance analytics
- Curriculum learning
- Training utilities
- Configuration management
"""

import argparse
import json
from typing import List
from .env import EmergencyResponseEnv
from .advanced_agents import create_agent, BaseAgent
from .graders import create_grader_for_task
from .analytics import PerformanceAnalyzer
from .training import TrainingSession, CurriculumLearner
from .config import create_experiment_config


def run_advanced_inference(
    experiment: str = "baseline_comparison",
    output_file: str = "advanced_results.json"
):
    """
    Run advanced inference with all features.
    
    Args:
        experiment: Name of predefined experiment
        output_file: Output file for results
    """
    print("\n" + "=" * 80)
    print("ADVANCED EMERGENCY RESPONSE INFERENCE")
    print("=" * 80)
    
    # Load experiment configuration
    config = create_experiment_config(experiment)
    
    print(f"\n📋 Experiment: {experiment.upper().replace('_', ' ')}")
    print(f"Description: {config['description']}")
    print(f"Episodes: {config['num_episodes']}")
    
    # Initialize analytics
    analyzer = PerformanceAnalyzer()
    
    # Run experiments
    all_results = {
        "experiment": experiment,
        "config": config,
        "episodes": []
    }
    
    tasks = config.get("tasks", ["medium"])
    agents = config.get("agents", ["priority"])
    num_episodes = config.get("num_episodes", 10)
    
    episode_count = 0
    for task in tasks:
        for agent_type in agents:
            print(f"\n{'─' * 80}")
            print(f"Running: Task={task}, Agent={agent_type}")
            print(f"{'─' * 80}")
            
            # Run episodes for this configuration
            episodes_per_config = num_episodes // (len(tasks) * len(agents))
            
            for episode_num in range(episodes_per_config):
                episode_count += 1
                
                # Create environment and agent
                env = EmergencyResponseEnv(task_difficulty=task)
                agent = create_agent(env, agent_type)
                
                # Run episode
                state = env.reset()
                total_reward = 0.0
                step_history = []
                
                done = False
                while not done:
                    action = agent.get_action(state)
                    next_state, reward, done, info = env.step(action)
                    step_history.append((state, action, reward, done))
                    total_reward += reward
                    state = next_state
                
                # Evaluate
                grader = create_grader_for_task(task)
                metrics = grader.evaluate_episode(env, step_history)
                
                # Record
                analyzer.add_episode(
                    episode_number=episode_count,
                    task_difficulty=task,
                    agent_name=agent_type,
                    total_reward=total_reward,
                    metrics=metrics,
                    env_stats={
                        "step_count": env.step_count,
                        "emergencies_handled": sum(1 for e in env.emergencies if e["assigned_ambulance"]),
                        "high_severity_handled": env.high_severity_handled,
                        "avg_response_time": env.total_response_time / max(1, sum(1 for e in env.emergencies if e["assigned_ambulance"])),
                        "unhandled_emergencies": sum(1 for e in env.emergencies if not e["assigned_ambulance"])
                    }
                )
                
                all_results["episodes"].append({
                    "episode": episode_count,
                    "task": task,
                    "agent": agent_type,
                    "reward": total_reward,
                    "score": metrics["final_score"],
                    "metrics": metrics
                })
                
                if (episode_num + 1) % max(1, episodes_per_config // 2) == 0 or episode_num == 0:
                    print(f"  Episode {episode_num + 1}/{episodes_per_config}: " +
                          f"Score={metrics['final_score']:.3f}, Reward={total_reward:.3f}")
    
    # Summary
    print("\n" + "=" * 80)
    print("EXPERIMENT RESULTS")
    print("=" * 80)
    
    analyzer.print_summary()
    
    # Export results
    all_results["summary_by_difficulty"] = analyzer.get_summary_by_difficulty()
    all_results["summary_by_agent"] = analyzer.get_summary_by_agent()
    
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Results saved to {output_file}")
    
    return all_results


def run_curriculum_training(
    agent_type: str = "adaptive",
    num_episodes: int = 30,
    output_file: str = "curriculum_results.json"
):
    """Run curriculum learning training."""
    print("\n" + "=" * 80)
    print("CURRICULUM LEARNING TRAINING")
    print("=" * 80)
    print(f"Agent: {agent_type}")
    print(f"Total Episodes: {num_episodes}")
    
    # Create analyzer
    analyzer = PerformanceAnalyzer()
    
    # Create curriculum
    curriculum = CurriculumLearner()
    
    # Training loop
    episode_count = 0
    for phase in range(num_episodes):
        # Select task based on curriculum
        task = curriculum.get_next_task()
        
        # Create environment and agent
        env = EmergencyResponseEnv(task_difficulty=task)
        agent = create_agent(env, agent_type)
        
        # Run episode
        state = env.reset()
        total_reward = 0.0
        step_history = []
        
        done = False
        while not done:
            action = agent.get_action(state)
            next_state, reward, done, info = env.step(action)
            step_history.append((state, action, reward, done))
            total_reward += reward
            state = next_state
        
        # Evaluate
        grader = create_grader_for_task(task)
        metrics = grader.evaluate_episode(env, step_history)
        
        # Record
        analyzer.add_episode(
            episode_number=phase + 1,
            task_difficulty=task,
            agent_name=agent_type,
            total_reward=total_reward,
            metrics=metrics,
            env_stats={"step_count": env.step_count}
        )
        
        # Curriculum update
        curriculum.record_score(task, metrics["final_score"])
        
        episode_count += 1
        
        if (phase + 1) % 5 == 0:
            print(f"  Phase {phase + 1}/{num_episodes}: Task={task}, Score={metrics['final_score']:.3f}")
    
    print("\n" + curriculum.get_progress_report())
    
    # Export
    results = {
        "training_type": "curriculum_learning",
        "agent": agent_type,
        "total_episodes": num_episodes,
        "curriculum_progress": curriculum.task_scores,
        "summary": analyzer.get_summary_by_difficulty()
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to {output_file}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advanced Emergency Response Inference with All Features"
    )
    parser.add_argument(
        "--mode",
        choices=["experiment", "curriculum"],
        default="experiment",
        help="Mode: experiment runs predefined experiments, curriculum runs curriculum learning"
    )
    parser.add_argument(
        "--experiment",
        choices=[
            "quick_test", "baseline_comparison", "curriculum_training",
            "agent_evolution", "ensemble_evaluation"
        ],
        default="baseline_comparison",
        help="Experiment to run"
    )
    parser.add_argument(
        "--agent",
        choices=["heuristic", "priority", "resource", "adaptive", "ensemble", "llm"],
        default="adaptive",
        help="Agent type for curriculum learning"
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=30,
        help="Number of episodes for curriculum learning"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="advanced_results.json",
        help="Output file for results"
    )
    
    args = parser.parse_args()
    
    if args.mode == "experiment":
        run_advanced_inference(
            experiment=args.experiment,
            output_file=args.output
        )
    else:
        run_curriculum_training(
            agent_type=args.agent,
            num_episodes=args.episodes,
            output_file=args.output
        )
