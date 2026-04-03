"""
Configuration Management for Emergency Response Environment

Centralized configuration for environment parameters, agent settings, and experiment configs.
"""

import json
import yaml
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class EnvironmentConfig:
    """Environment configuration."""
    num_emergencies: int
    num_ambulances: int
    num_hospitals: int
    grid_size: int
    max_steps: int
    task_difficulty: str


@dataclass
class AgentConfig:
    """Agent configuration."""
    agent_type: str  # "heuristic", "priority", "resource", "adaptive", "ensemble", "llm"
    learning_rate: float = 0.1
    exploration_rate: float = 0.1
    memory_size: int = 1000


@dataclass
class TrainingConfig:
    """Training configuration."""
    num_episodes: int
    curriculum_learning: bool
    task_selection_strategy: str  # "balanced", "weak", "progressive"
    curriculum_threshold: float = 0.70
    batch_size: int = 5


class ConfigManager:
    """Manage configurations for experiments."""
    
    # Default configurations
    DEFAULTS = {
        "easy": {
            "num_emergencies": 3,
            "num_ambulances": 6,
            "num_hospitals": 3,
            "grid_size": 10,
            "max_steps": 30,
            "task_difficulty": "easy"
        },
        "medium": {
            "num_emergencies": 5,
            "num_ambulances": 6,
            "num_hospitals": 3,
            "grid_size": 10,
            "max_steps": 50,
            "task_difficulty": "medium"
        },
        "hard": {
            "num_emergencies": 8,
            "num_ambulances": 6,
            "num_hospitals": 3,
            "grid_size": 10,
            "max_steps": 100,
            "task_difficulty": "hard"
        }
    }
    
    def __init__(self, config_file: str = None):
        """Initialize config manager."""
        self.config = {}
        
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """Load configuration from YAML or JSON file."""
        if config_file.endswith('.yaml') or config_file.endswith('.yml'):
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
    
    def save_to_file(self, config_file: str):
        """Save configuration to file."""
        if config_file.endswith('.yaml') or config_file.endswith('.yml'):
            with open(config_file, 'w') as f:
                yaml.dump(self.config, f)
        else:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
    
    def get_environment_config(self, task_difficulty: str) -> Dict[str, Any]:
        """Get environment config for task difficulty."""
        return self.DEFAULTS.get(task_difficulty, self.DEFAULTS["medium"])
    
    def get_agent_config(self, agent_type: str = "priority") -> Dict[str, Any]:
        """Get agent configuration."""
        return {
            "agent_type": agent_type,
            "learning_rate": 0.1,
            "exploration_rate": 0.1,
            "memory_size": 1000
        }
    
    def get_training_config(
        self,
        num_episodes: int = 20,
        curriculum: bool = False,
        strategy: str = "balanced"
    ) -> Dict[str, Any]:
        """Get training configuration."""
        return {
            "num_episodes": num_episodes,
            "curriculum_learning": curriculum,
            "task_selection_strategy": strategy,
            "curriculum_threshold": 0.70,
            "batch_size": 5
        }
    
    def merge_config(self, config_dict: Dict[str, Any]):
        """Merge with provided configuration."""
        self.config.update(config_dict)
    
    def export_to_yaml(self, filename: str):
        """Export config to YAML."""
        self.save_to_file(filename)


# Predefined experiment configurations

EXPERIMENT_CONFIGS = {
    "quick_test": {
        "description": "Quick test with small episodes",
        "num_episodes": 3,
        "curriculum_learning": False,
        "tasks": ["easy"],
        "agents": ["priority", "resource"]
    },
    "baseline_comparison": {
        "description": "Compare baseline agents on all difficulties",
        "num_episodes": 10,
        "curriculum_learning": False,
        "tasks": ["easy", "medium", "hard"],
        "agents": ["heuristic", "priority", "resource", "adaptive"]
    },
    "curriculum_training": {
        "description": "Full curriculum learning: easy → medium → hard",
        "num_episodes": 30,
        "curriculum_learning": True,
        "strategy": "progressive",
        "tasks": ["easy", "medium", "hard"],
        "agents": ["adaptive"]
    },
    "agent_evolution": {
        "description": "Train single agent on all difficulties with curriculum",
        "num_episodes": 50,
        "curriculum_learning": True,
        "strategy": "progressive",
        "agent": "adaptive",
        "focus": "learning_progression"
    },
    "ensemble_evaluation": {
        "description": "Evaluate ensemble agent performance",
        "num_episodes": 20,
        "curriculum_learning": False,
        "tasks": ["easy", "medium", "hard"],
        "agents": ["priority", "resource", "ensemble"]
    }
}


def create_experiment_config(experiment_name: str) -> Dict[str, Any]:
    """Create configuration for predefined experiment."""
    if experiment_name not in EXPERIMENT_CONFIGS:
        raise ValueError(f"Unknown experiment: {experiment_name}")
    
    return EXPERIMENT_CONFIGS[experiment_name]


def get_experiment_recommendations() -> str:
    """Get recommendations for experiments."""
    output = "\n📋 RECOMMENDED EXPERIMENTS\n"
    output += "─" * 70 + "\n"
    
    for name, config in EXPERIMENT_CONFIGS.items():
        output += f"\n{name.upper().replace('_', ' ')}\n"
        output += f"  Description: {config['description']}\n"
        output += f"  Episodes: {config['num_episodes']}\n"
        if 'agents' in config:
            output += f"  Agents: {', '.join(config['agents'])}\n"
    
    output += "\n" + "─" * 70 + "\n"
    output += "💡 TIP: Start with 'quick_test' for validation, then run 'curriculum_training'\n"
    
    return output


# Configuration templates for different scenarios

SCENARIO_CONFIGS = {
    "optimization_focus": {
        "reward_weights": {
            "priority_handling": 0.5,
            "response_speed": 0.3,
            "resource_usage": 0.2
        },
        "difficulty_progression": ["easy", "medium", "hard"],
        "focus": "maximizing final score"
    },
    "response_speed_focus": {
        "reward_weights": {
            "priority_handling": 0.3,
            "response_speed": 0.5,
            "resource_usage": 0.2
        },
        "difficulty_progression": ["easy", "medium", "hard"],
        "focus": "minimizing response time"
    },
    "resource_efficiency_focus": {
        "reward_weights": {
            "priority_handling": 0.3,
            "response_speed": 0.2,
            "resource_usage": 0.5
        },
        "difficulty_progression": ["easy", "medium", "hard"],
        "focus": "maximizing resource utilization"
    }
}


def configure_reward_weights(scenario: str) -> Dict[str, float]:
    """Get reward weights for scenario."""
    return SCENARIO_CONFIGS.get(scenario, SCENARIO_CONFIGS["optimization_focus"])["reward_weights"]
