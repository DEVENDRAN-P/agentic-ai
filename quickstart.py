#!/usr/bin/env python3
"""
QUICK START GUIDE - Smart Emergency Response Environment
Run this script to verify everything is set up correctly.

Usage: python quickstart.py
"""

import os
import json
from pathlib import Path


BANNER = """
╔══════════════════════════════════════════════════════════════╗
║     SMART EMERGENCY RESPONSE ENVIRONMENT - HACKATHON         ║
║                  Quick Start Configuration                   ║
╚══════════════════════════════════════════════════════════════╝
"""


def check_project_structure():
    """Verify all required files exist."""
    print("\n📁 Checking Project Structure...")
    
    required_files = {
        "src/env.py": "Main environment",
        "src/graders.py": "Scoring system",
        "src/inference.py": "Agent interaction",
        "configs/openenv.yaml": "Environment config",
        "requirements.txt": "Dependencies",
        "README.md": "Documentation",
        "Dockerfile": "Deployment",
        ".github/agents/emergency-response-designer.agent.md": "VS Code agent",
        "tests/test_env.py": "Tests"
    }
    
    all_good = True
    for file, desc in required_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✓ {file:45} ({size:>6} bytes) - {desc}")
        else:
            print(f"  ✗ {file:45} MISSING")
            all_good = False
    
    return all_good


def show_quick_commands():
    """Display quick start commands."""
    print("\n⚡ Quick Start Commands")
    print("─" * 70)
    
    commands = [
        ("Install dependencies", "pip install -r requirements.txt"),
        ("Run tests", "python tests/test_env.py"),
        ("Run easy task (random agent)", "python src/inference.py --task easy --episodes 5 --agent random"),
        ("Run easy task (heuristic agent)", "python src/inference.py --task easy --episodes 5 --agent heuristic"),
        ("Run medium task", "python src/inference.py --task medium --episodes 10"),
        ("Run hard task", "python src/inference.py --task hard --episodes 20"),
        ("Save results to file", "python src/inference.py --task medium --output results.json"),
        ("Build Docker image", "docker build -t emergency-response ."),
        ("Run Docker container", "docker run emergency-response --task medium --episodes 5"),
    ]
    
    for desc, cmd in commands:
        print(f"\n  📌 {desc}")
        print(f"     $ {cmd}")


def show_project_overview():
    """Display project overview."""
    print("\n🎯 Project Overview")
    print("─" * 70)
    
    overview = {
        "Problem": "Optimize emergency response by assigning ambulances to emergencies and selecting hospitals",
        "Environment": "EmergencyResponseEnv - OpenEnv-compatible with 3 task difficulties",
        "State Space": "Emergencies, ambulances, hospitals, traffic level",
        "Action Space": "Select ambulance ID, emergency ID, hospital ID",
        "Reward Function": "0.5*priority + 0.3*speed + 0.2*resource",
        "Metrics": "Priority Handling, Response Speed, Resource Usage",
        "Scoring": "Normalized to [0.0, 1.0]",
        "Task Levels": "Easy (basic), Medium (prioritization), Hard (complex)",
    }
    
    for key, value in overview.items():
        print(f"  • {key:20} {value}")


def show_reward_breakdown():
    """Display reward function details."""
    print("\n💰 Reward Function Breakdown")
    print("─" * 70)
    
    print("  Formula: total_reward = 0.5*priority + 0.3*speed + 0.2*resource")
    print()
    print("  ┌─ Priority Handling (50% weight)")
    print("  │  ├─ Reward: +0.5 for assigning high-severity first")
    print("  │  └─ Penalty: -0.5 for ignoring critical cases")
    print()
    print("  ├─ Response Speed (30% weight)")
    print("  │  ├─ Reward: Up to +0.3 for fast response")
    print("  │  └─ Penalty: -0.3 for delays")
    print()
    print("  └─ Resource Usage (20% weight)")
    print("     ├─ Reward: Up to +0.2 for efficient allocation")
    print("     └─ Penalty: -0.1 for underutilization")


def show_task_progression():
    """Display task progression details."""
    print("\n📊 Task Progression (Easy → Hard)")
    print("─" * 70)
    
    tasks = {
        "EASY 🟢": {
            "Emergencies": "2-3",
            "Ambulances": "6 (all available)",
            "Hospital Capacity": "10 per hospital",
            "Traffic": "Normal (1.0x)",
            "Focus": "Basic assignment"
        },
        "MEDIUM 🟡": {
            "Emergencies": "4-5",
            "Ambulances": "6 (2 busy initially)",
            "Hospital Capacity": "4 per hospital",
            "Traffic": "Moderate (1.5x)",
            "Focus": "Prioritization under constraints"
        },
        "HARD 🔴": {
            "Emergencies": "6-8 (dynamic spawn)",
            "Ambulances": "6 (4 busy initially)",
            "Hospital Capacity": "2 per hospital",
            "Traffic": "Heavy (2.0x)",
            "Focus": "Complex decision-making"
        }
    }
    
    for task_name, params in tasks.items():
        print(f"\n  {task_name}")
        for key, value in params.items():
            print(f"    • {key:18} {value}")


def show_expected_scores():
    """Display expected performance scores."""
    print("\n📈 Expected Performance Scores")
    print("─" * 70)
    
    scores = {
        "Random Agent": {"easy": "0.35-0.45", "medium": "0.40-0.50", "hard": "0.30-0.40"},
        "Heuristic Agent": {"easy": "0.70-0.80", "medium": "0.60-0.70", "hard": "0.45-0.55"},
        "LLM Agent": {"easy": "0.85-0.95", "medium": "0.75-0.85", "hard": "0.65-0.75"},
    }
    
    for agent_type, task_scores in scores.items():
        print(f"\n  {agent_type}")
        for difficulty, score_range in task_scores.items():
            print(f"    • {difficulty:6} → {score_range}")


def show_file_descriptions():
    """Display detailed file descriptions."""
    print("\n📚 Core Files Description")
    print("─" * 70)
    
    files = {
        "src/env.py": [
            "Main OpenEnv environment class",
            "- EmergencyResponseEnv(task_difficulty: str)",
            "- reset() → state",
            "- step(action) → (state, reward, done, info)",
            "- Three task difficulties: easy, medium, hard"
        ],
        "src/graders.py": [
            "Grading/scoring system aligned with hackathon criteria",
            "- EmergencyResponseGrader (base)",
            "- EasyTaskGrader, MediumTaskGrader, HardTaskGrader",
            "- 3-metric evaluation: priority, speed, resource",
            "- Output normalized to [0.0, 1.0]"
        ],
        "src/inference.py": [
            "Template for AI agent interaction",
            "- RandomBaselineAgent (for baseline comparison)",
            "- SmartHeuristicAgent (priority-based rules)",
            "- run_episode() and run_inference() functions",
            "- CLI interface: --task, --episodes, --agent, --output"
        ],
        "configs/openenv.yaml": [
            "Complete environment specification document",
            "- Defines state/action spaces with examples",
            "- Documents reward function formula and components",
            "- Specifies grading metrics and final score calculation",
            "- Configuration for all task difficulties"
        ],
        "README.md": [
            "Comprehensive documentation (1500+ lines)",
            "- Problem statement and real-world impact",
            "- Detailed environment design explanation",
            "- Reward function breakdown with examples",
            "- Task progression rubrics and expected scores",
            "- Quick start guide and deployment options"
        ]
    }
    
    for file, lines in files.items():
        print(f"\n  {file}")
        for line in lines:
            print(f"    {line}")


def main():
    os.chdir(Path(__file__).parent)
    
    print(BANNER)
    
    # Check structure
    if check_project_structure():
        print("\n  ✅ All files present and accounted for!")
    else:
        print("\n  ⚠️  Some files missing - check above")
    
    # Show overview
    show_project_overview()
    
    # Show reward breakdown
    show_reward_breakdown()
    
    # Show task progression
    show_task_progression()
    
    # Show expected scores
    show_expected_scores()
    
    # Show file descriptions
    show_file_descriptions()
    
    # Show quick commands
    show_quick_commands()
    
    # Final instructions
    print("\n" + "=" * 70)
    print("🚀 NEXT STEPS")
    print("=" * 70)
    print("""
  1. Install dependencies:
     pip install -r requirements.txt

  2. Run quick test:
     python tests/test_env.py

  3. Try baseline agent:
     python src/inference.py --task easy --episodes 5 --agent heuristic

  4. Check results:
     cat results.json

  5. Implement your LLM agent:
     - Update inference.py with your agent logic
     - Call LLM API to reason about state
     - Return valid actions

  6. Deploy:
     - Docker: docker build -t emergency-response . && docker run ...
     - Hugging Face Spaces: Push repo to HF Space

📖 See README.md for full documentation and examples
🎯 See .github/agents/emergency-response-designer.agent.md for VS Code agent help
⚙️  See configs/openenv.yaml for full specification
    """)
    
    print("=" * 70)
    print("Happy coding! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()
