"""
Training Utilities for Multi-Task and Curriculum Learning

Provides tools for training agents across multiple tasks,
with curriculum learning support.
"""

from typing import Dict, List, Tuple, Any, Callable
import json
from .env import EmergencyResponseEnv
from .graders import create_grader_for_task
from .analytics import PerformanceAnalyzer, EpisodeMetrics


class CurriculumLearner:
    """
    Implements curriculum learning: progressively harder tasks.
    
    Strategy:
    1. Train on easy until performance threshold
    2. Transition to medium
    3. Transition to hard
    4. Fine-tune on mixed difficulties
    """
    
    def __init__(
        self,
        performance_threshold: float = 0.70,
        min_episodes_per_task: int = 5,
        max_episodes_per_task: int = 50
    ):
        self.performance_threshold = performance_threshold
        self.min_episodes_per_task = min_episodes_per_task
        self.max_episodes_per_task = max_episodes_per_task
        self.current_task = "easy"
        self.task_scores: Dict[str, List[float]] = {
            "easy": [],
            "medium": [],
            "hard": []
        }
    
    def should_advance(self) -> bool:
        """Check if ready to advance to harder task."""
        if len(self.task_scores[self.current_task]) < self.min_episodes_per_task:
            return False
        
        recent_scores = self.task_scores[self.current_task][-10:]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        return avg_score >= self.performance_threshold
    
    def advance_to_next_task(self) -> bool:
        """Advance to next difficulty level."""
        tasks = ["easy", "medium", "hard"]
        current_idx = tasks.index(self.current_task)
        
        if current_idx < len(tasks) - 1:
            self.current_task = tasks[current_idx + 1]
            return True
        
        return False
    
    def record_score(self, task: str, score: float):
        """Record score for task."""
        if task in self.task_scores:
            self.task_scores[task].append(score)
    
    def get_next_task(self) -> str:
        """Get next task to train on."""
        if self.should_advance() and self.current_task != "hard":
            self.advance_to_next_task()
        
        return self.current_task
    
    def get_progress_report(self) -> str:
        """Get human-readable progress report."""
        report = f"\nCurriculum Learning Progress\n"
        report += f"{'─' * 50}\n"
        report += f"Current Task: {self.current_task.upper()}\n\n"
        
        for task, scores in self.task_scores.items():
            if scores:
                avg = sum(scores) / len(scores)
                best = max(scores)
                report += f"{task.upper()}: {len(scores)} episodes, avg={avg:.3f}, best={best:.3f}\n"
        
        return report


class MultiTaskTrainer:
    """
    Train agent on multiple task difficulties with mixed curriculum.
    
    Supports:
    - Task rotation
    - Performance tracking per task
    - Adaptive task selection
    """
    
    def __init__(self):
        self.task_performance: Dict[str, List[float]] = {
            "easy": [],
            "medium": [],
            "hard": []
        }
        self.episode_count = 0
    
    def select_next_task(self, strategy: str = "balanced") -> str:
        """Select next task to train on."""
        if strategy == "balanced":
            # Rotate through tasks
            tasks = ["easy", "medium", "hard"]
            return tasks[self.episode_count % 3]
        
        elif strategy == "weak":
            # Focus on weakest task
            avg_performance = {
                task: (sum(scores) / len(scores)) if scores else 0.0
                for task, scores in self.task_performance.items()
            }
            return min(avg_performance.keys(), key=lambda k: avg_performance[k])
        
        elif strategy == "progressive":
            # Progressive: easy -> medium -> hard
            if not self.task_performance["medium"]:
                return "easy"
            elif not self.task_performance["hard"]:
                return "medium"
            else:
                return "hard"
        
        else:
            return "medium"
    
    def record_performance(self, task: str, score: float):
        """Record performance on task."""
        if task in self.task_performance:
            self.task_performance[task].append(score)
        self.episode_count += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get training summary."""
        summary = {
            "total_episodes": self.episode_count,
            "task_summaries": {}
        }
        
        for task, scores in self.task_performance.items():
            if scores:
                summary["task_summaries"][task] = {
                    "episodes": len(scores),
                    "average_score": sum(scores) / len(scores),
                    "best_score": max(scores),
                    "worst_score": min(scores),
                    "improvement": scores[-1] - scores[0] if len(scores) > 1 else 0
                }
        
        return summary


class TrainingSession:
    """Complete training session with logging and analytics."""
    
    def __init__(
        self,
        agent_factory: Callable,
        analyzer: PerformanceAnalyzer,
        curriculum: bool = False
    ):
        self.agent_factory = agent_factory
        self.analyzer = analyzer
        self.curriculum = CurriculumLearner() if curriculum else None
        self.multi_trainer = MultiTaskTrainer()
        self.session_data = {
            "start_time": None,
            "end_time": None,
            "total_episodes": 0,
            "episodes_by_task": {"easy": 0, "medium": 0, "hard": 0}
        }
    
    def run_training(
        self,
        num_episodes: int,
        agent_name: str = "TrainingAgent",
        task_selection: str = "balanced"
    ) -> Dict[str, Any]:
        """Run training session."""
        import time
        import datetime
        
        self.session_data["start_time"] = datetime.datetime.now().isoformat()
        
        for episode in range(num_episodes):
            # Select task
            if self.curriculum:
                task = self.curriculum.get_next_task()
            else:
                task = self.multi_trainer.select_next_task(task_selection)
            
            # Create environment and agent
            env = EmergencyResponseEnv(task_difficulty=task)
            agent = self.agent_factory(env)
            
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
            
            # Get metrics
            grader = create_grader_for_task(task)
            episode_metrics = grader.evaluate_episode(env, step_history)
            
            # Record
            self.analyzer.add_episode(
                episode_number=episode + 1,
                task_difficulty=task,
                agent_name=agent_name,
                total_reward=total_reward,
                metrics=episode_metrics,
                env_stats={
                    "step_count": env.step_count,
                    "emergencies_handled": sum(1 for e in env.emergencies if e["assigned_ambulance"]),
                    "high_severity_handled": env.high_severity_handled,
                    "avg_response_time": env.total_response_time / max(1, sum(1 for e in env.emergencies if e["assigned_ambulance"])),
                    "unhandled_emergencies": sum(1 for e in env.emergencies if not e["assigned_ambulance"])
                }
            )
            
            self.multi_trainer.record_performance(task, episode_metrics["final_score"])
            self.session_data["episodes_by_task"][task] += 1
            
            if self.curriculum:
                self.curriculum.record_score(task, episode_metrics["final_score"])
            
            # Progress update
            if (episode + 1) % 5 == 0:
                print(f"  Episode {episode + 1}/{num_episodes} - Task: {task}, Score: {episode_metrics['final_score']:.3f}")
        
        self.session_data["end_time"] = datetime.datetime.now().isoformat()
        self.session_data["total_episodes"] = num_episodes
        
        return self.get_session_report()
    
    def get_session_report(self) -> Dict[str, Any]:
        """Generate training session report."""
        report = {
            "session_data": self.session_data,
            "performance_summary": self.analyzer.get_summary_by_difficulty(),
            "agent_summary": self.analyzer.get_summary_by_agent(),
            "multi_task_summary": self.multi_trainer.get_summary()
        }
        
        if self.curriculum:
            report["curriculum_progress"] = self.curriculum.task_scores
        
        return report
    
    def export_report(self, filename: str = "training_report.json"):
        """Export training report to file."""
        report = self.get_session_report()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Training report saved to {filename}")
        print(self.multi_trainer.get_summary())
