"""
Analytics Module for Performance Analysis and Visualization

Provides detailed metrics, statistics, and insights into agent performance
across multiple dimensions.
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
import datetime


@dataclass
class EpisodeMetrics:
    """Metrics for a single episode."""
    episode_number: int
    task_difficulty: str
    agent_name: str
    total_reward: float
    final_score: float
    priority_handling: float
    response_speed: float
    resource_usage: float
    num_steps: int
    emergencies_handled: int
    high_severity_handled: int
    avg_response_time: float
    unhandled_emergencies: int
    timestamp: str


class PerformanceAnalyzer:
    """Analyzes agent performance across episodes."""
    
    def __init__(self):
        self.episodes: List[EpisodeMetrics] = []
    
    def add_episode(
        self,
        episode_number: int,
        task_difficulty: str,
        agent_name: str,
        total_reward: float,
        metrics: Dict[str, float],
        env_stats: Dict[str, Any]
    ):
        """Record episode metrics."""
        episode = EpisodeMetrics(
            episode_number=episode_number,
            task_difficulty=task_difficulty,
            agent_name=agent_name,
            total_reward=total_reward,
            final_score=metrics.get("final_score", 0.0),
            priority_handling=metrics.get("priority_handling", 0.0),
            response_speed=metrics.get("response_speed", 0.0),
            resource_usage=metrics.get("resource_usage", 0.0),
            num_steps=env_stats.get("step_count", 0),
            emergencies_handled=env_stats.get("emergencies_handled", 0),
            high_severity_handled=env_stats.get("high_severity_handled", 0),
            avg_response_time=env_stats.get("avg_response_time", 0.0),
            unhandled_emergencies=env_stats.get("unhandled_emergencies", 0),
            timestamp=datetime.datetime.now().isoformat()
        )
        self.episodes.append(episode)
    
    def get_summary_by_difficulty(self) -> Dict[str, Dict[str, float]]:
        """Get summary statistics grouped by difficulty."""
        summary = {}
        
        for difficulty in ["easy", "medium", "hard"]:
            episodes = [e for e in self.episodes if e.task_difficulty == difficulty]
            
            if episodes:
                scores = [e.final_score for e in episodes]
                rewards = [e.total_reward for e in episodes]
                
                summary[difficulty] = {
                    "num_episodes": len(episodes),
                    "avg_score": float(np.mean(scores)),
                    "std_score": float(np.std(scores)),
                    "min_score": float(np.min(scores)),
                    "max_score": float(np.max(scores)),
                    "avg_reward": float(np.mean(rewards)),
                    "avg_response_time": float(np.mean([e.avg_response_time for e in episodes])),
                    "priority_handling_avg": float(np.mean([e.priority_handling for e in episodes])),
                    "resource_usage_avg": float(np.mean([e.resource_usage for e in episodes])),
                }
        
        return summary
    
    def get_summary_by_agent(self) -> Dict[str, Dict[str, float]]:
        """Get summary statistics grouped by agent."""
        summary = {}
        
        agent_names = set(e.agent_name for e in self.episodes)
        
        for agent_name in agent_names:
            episodes = [e for e in self.episodes if e.agent_name == agent_name]
            
            scores = [e.final_score for e in episodes]
            summary[agent_name] = {
                "num_episodes": len(episodes),
                "avg_score": float(np.mean(scores)) if scores else 0,
                "std_score": float(np.std(scores)) if scores else 0,
                "best_score": float(np.max(scores)) if scores else 0,
                "worst_score": float(np.min(scores)) if scores else 0,
            }
        
        return summary
    
    def get_learning_curve(self, agent_name: str, task_difficulty: str) -> Dict[str, List]:
        """Get learning curve data for plotting."""
        episodes = [
            e for e in self.episodes 
            if e.agent_name == agent_name and e.task_difficulty == task_difficulty
        ]
        
        return {
            "episode_numbers": [e.episode_number for e in episodes],
            "scores": [e.final_score for e in episodes],
            "rewards": [e.total_reward for e in episodes],
            "response_times": [e.avg_response_time for e in episodes]
        }
    
    def export_to_json(self, filename: str):
        """Export analytics to JSON file."""
        data = {
            "episodes": [asdict(e) for e in self.episodes],
            "summary_by_difficulty": self.get_summary_by_difficulty(),
            "summary_by_agent": self.get_summary_by_agent(),
            "total_episodes": len(self.episodes)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def print_summary(self):
        """Print human-readable summary."""
        print("\n" + "=" * 80)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"\nTotal Episodes Run: {len(self.episodes)}")
        
        # By difficulty
        print("\n📊 PERFORMANCE BY DIFFICULTY")
        print("-" * 80)
        for difficulty, stats in self.get_summary_by_difficulty().items():
            print(f"\n{difficulty.upper()}:")
            print(f"  Episodes: {stats['num_episodes']}")
            print(f"  Avg Score: {stats['avg_score']:.3f} ± {stats['std_score']:.3f}")
            print(f"  Score Range: [{stats['min_score']:.3f}, {stats['max_score']:.3f}]")
            print(f"  Avg Response Time: {stats['avg_response_time']:.1f}s")
        
        # By agent
        print("\n🤖 PERFORMANCE BY AGENT")
        print("-" * 80)
        for agent_name, stats in self.get_summary_by_agent().items():
            print(f"\n{agent_name}:")
            print(f"  Episodes: {stats['num_episodes']}")
            print(f"  Avg Score: {stats['avg_score']:.3f} ± {stats['std_score']:.3f}")
            print(f"  Best Score: {stats['best_score']:.3f}")
        
        print("\n" + "=" * 80)


class MetricsCalculator:
    """Calculate detailed metrics from episode data."""
    
    @staticmethod
    def calculate_priority_effectiveness(
        high_severity_handled: int,
        total_high_severity: int,
        avg_wait_time_high_severity: float
    ) -> float:
        """
        Calculate how effectively agent prioritizes high-severity cases.
        
        Factors:
        - % of high-severity handled
        - Average wait time for high-severity cases
        """
        if total_high_severity == 0:
            return 1.0
        
        handling_ratio = high_severity_handled / total_high_severity
        wait_penalty = min(avg_wait_time_high_severity / 30.0, 0.3)
        
        return max(0.0, handling_ratio - wait_penalty)
    
    @staticmethod
    def calculate_response_efficiency(
        avg_response_time: float,
        task_difficulty: str
    ) -> float:
        """Calculate response time efficiency relative to difficulty."""
        thresholds = {
            "easy": 20.0,
            "medium": 30.0,
            "hard": 40.0
        }
        
        threshold = thresholds.get(task_difficulty, 30.0)
        efficiency = 1.0 - (avg_response_time / threshold)
        
        return max(0.0, min(1.0, efficiency))
    
    @staticmethod
    def calculate_resource_balance(
        ambulance_utilization: float,
        hospital_load_variance: float,
        max_hospitals: int
    ) -> float:
        """Calculate how well resources are balanced."""
        utilization_score = min(ambulance_utilization, 1.0)
        
        # Prefer low variance (balanced load)
        variance_score = 1.0 - min(hospital_load_variance / max_hospitals, 1.0)
        
        return 0.6 * utilization_score + 0.4 * variance_score


class ComparisonAnalyzer:
    """Compare performance across different dimensions."""
    
    def __init__(self, analyzer: PerformanceAnalyzer):
        self.analyzer = analyzer
    
    def agent_comparison(self) -> str:
        """Compare agents by average score."""
        summary = self.analyzer.get_summary_by_agent()
        
        if not summary:
            return "No data for comparison"
        
        # Sort by average score
        sorted_agents = sorted(
            summary.items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        output = "\n🏆 AGENT RANKINGS (by average score)\n"
        output += "─" * 60 + "\n"
        
        for rank, (agent_name, stats) in enumerate(sorted_agents, 1):
            output += f"{rank}. {agent_name:20} → {stats['avg_score']:.3f} (±{stats['std_score']:.3f})\n"
        
        return output
    
    def difficulty_comparison(self) -> str:
        """Compare task difficulties."""
        summary = self.analyzer.get_summary_by_difficulty()
        
        output = "\n📈 TASK DIFFICULTY COMPARISON\n"
        output += "─" * 60 + "\n"
        
        for difficulty, stats in summary.items():
            output += f"\n{difficulty.upper()}:\n"
            output += f"  Episodes: {stats['num_episodes']}\n"
            output += f"  Average Score: {stats['avg_score']:.3f}\n"
            output += f"  Avg Response Time: {stats['avg_response_time']:.1f}s\n"
        
        return output


def create_performance_report(analyzer: PerformanceAnalyzer, filename: str = "performance_report.txt"):
    """Generate comprehensive performance report."""
    report = []
    report.append("=" * 80)
    report.append("EMERGENCY RESPONSE ENVIRONMENT - PERFORMANCE REPORT")
    report.append("=" * 80)
    report.append(f"Report Time: {datetime.datetime.now().isoformat()}\n")
    
    # Summary statistics
    analyzer.print_summary()
    
    # Agent comparison
    comparator = ComparisonAnalyzer(analyzer)
    report.append(comparator.agent_comparison())
    report.append(comparator.difficulty_comparison())
    
    report_text = "\n".join(report)
    
    with open(filename, 'w') as f:
        f.write(report_text)
    
    return report_text
