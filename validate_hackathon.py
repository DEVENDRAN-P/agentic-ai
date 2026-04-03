#!/usr/bin/env python
"""
Hackathon Validation Script

Comprehensive validation of all project requirements for submission.
Checks:
- OpenEnv compliance (step, reset, state)
- Environment structure
- Grading system
- Inference capabilities
- Output format
- All test cases

Usage:
    python validate_hackathon.py
    
Output:
    Detailed report with pass/fail for each component
"""

import sys
import json
from typing import Dict, List, Tuple, Any

# Add path
sys.path.insert(0, '.')

def check_imports() -> Tuple[bool, str]:
    """Check if all required modules can be imported."""
    try:
        from src.env import EmergencyResponseEnv
        from src.graders import create_grader_for_task
        from src.inference import run_inference
        from src.advanced_agents import create_agent
        return True, "✓ All modules import successfully"
    except Exception as e:
        return False, f"✗ Import error: {e}"


def check_openenv_compliance() -> Tuple[bool, str]:
    """Check OpenEnv compliance: step, reset, state methods."""
    try:
        from src.env import EmergencyResponseEnv
        env = EmergencyResponseEnv("easy")
        
        # Check reset()
        state = env.reset()
        if not isinstance(state, dict):
            return False, "✗ reset() does not return dict"
        
        # Check state()
        state = env.state()
        if not isinstance(state, dict):
            return False, "✗ state() does not return dict"
        
        # Check step()
        action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
        result = env.step(action)
        if not isinstance(result, tuple) or len(result) != 4:
            return False, "✗ step() does not return (state, reward, done, info)"
        
        next_state, reward, done, info = result
        if not isinstance(next_state, dict):
            return False, "✗ step() state output not dict"
        if not isinstance(reward, (int, float)):
            return False, "✗ step() reward not numeric"
        if not isinstance(done, bool):
            return False, "✗ step() done not boolean"
        
        return True, "✓ OpenEnv compliance verified (step, reset, state)"
    except Exception as e:
        return False, f"✗ OpenEnv check failed: {e}"


def check_environment_structure() -> Tuple[bool, str]:
    """Check environment has required structure."""
    try:
        from src.env import EmergencyResponseEnv
        env = EmergencyResponseEnv("medium")
        state = env.state()
        
        # Check state components
        required_keys = ["emergencies", "ambulances", "hospitals", "traffic_level"]
        for key in required_keys:
            if key not in state:
                return False, f"✗ State missing key: {key}"
        
        # Check emergencies structure
        if not isinstance(state["emergencies"], list) or len(state["emergencies"]) == 0:
            return False, "✗ Emergencies not valid list"
        
        required_emergency_keys = ["id", "severity", "location", "time_waiting"]
        for e in state["emergencies"][:1]:
            for key in required_emergency_keys:
                if key not in e:
                    return False, f"✗ Emergency missing key: {key}"
        
        # Check ambulances structure
        if not isinstance(state["ambulances"], list):
            return False, "✗ Ambulances not valid list"
        
        # Check hospitals structure
        if not isinstance(state["hospitals"], list):
            return False, "✗ Hospitals not valid list"
        
        return True, "✓ Environment structure correct"
    except Exception as e:
        return False, f"✗ Environment structure check failed: {e}"


def check_grading_system() -> Tuple[bool, str]:
    """Check grading system works."""
    try:
        from src.env import EmergencyResponseEnv
        from src.graders import create_grader_for_task
        
        env = EmergencyResponseEnv("easy")
        grader = create_grader_for_task("easy")
        
        # Run episode to get history
        state = env.reset()
        step_history = []
        done = False
        steps = 0
        
        while not done and steps < 10:
            action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
            next_state, reward, done, info = env.step(action)
            step_history.append((state, action, reward, done))
            state = next_state
            steps += 1
        
        # Grade episode
        metrics = grader.evaluate_episode(env, step_history)
        
        # Check metrics
        required_metrics = ["priority_handling", "response_speed", "resource_usage", "final_score"]
        for metric in required_metrics:
            if metric not in metrics:
                return False, f"✗ Grader missing metric: {metric}"
        
        # Check score in valid range
        if not (0.0 <= metrics["final_score"] <= 1.0):
            return False, f"✗ Final score out of range: {metrics['final_score']}"
        
        return True, "✓ Grading system operational"
    except Exception as e:
        return False, f"✗ Grading system check failed: {e}"


def check_task_progression() -> Tuple[bool, str]:
    """Check all task difficulties work."""
    try:
        from src.env import EmergencyResponseEnv
        
        for difficulty in ["easy", "medium", "hard"]:
            env = EmergencyResponseEnv(difficulty)
            state = env.reset()
            
            # Take one step
            action = {"ambulance_id": 1, "emergency_id": 1, "hospital_id": 1}
            next_state, reward, done, info = env.step(action)
            
            if not isinstance(reward, (int, float)):
                return False, f"✗ {difficulty} task doesn't return valid reward"
        
        return True, "✓ All task difficulties operational (easy, medium, hard)"
    except Exception as e:
        return False, f"✗ Task progression check failed: {e}"


def check_inference_output() -> Tuple[bool, str]:
    """Check inference output format."""
    try:
        from src.inference import run_inference
        import io
        from contextlib import redirect_stdout
        
        # Capture output
        f = io.StringIO()
        with redirect_stdout(f):
            result = run_inference(
                task_difficulty="easy",
                num_episodes=2,
                agent_type="heuristic",
                use_open_env_format=True,
                verbose=False
            )
        
        output = f.getvalue()
        
        # Check format
        if "[START]" not in output:
            return False, "✗ Missing [START] tag"
        if "[END]" not in output:
            return False, "✗ Missing [END] tag"
        
        # Check result structure
        if "episodes" not in result or "statistics" not in result:
            return False, "✗ Result structure invalid"
        
        return True, "✓ Inference output format correct (OpenEnv compliant)"
    except Exception as e:
        return False, f"✗ Inference output check failed: {e}"


def check_agents() -> Tuple[bool, str]:
    """Check all agent types available."""
    try:
        from src.advanced_agents import create_agent
        from src.env import EmergencyResponseEnv
        
        env = EmergencyResponseEnv("easy")
        agents = ["priority", "resource", "adaptive", "ensemble", "llm"]
        
        for agent_type in agents:
            try:
                agent = create_agent(env, agent_type)
                if agent is None:
                    return False, f"✗ Agent '{agent_type}' creation failed"
            except Exception as e:
                return False, f"✗ Agent '{agent_type}' error: {e}"
        
        return True, "✓ All 5 agent types available"
    except Exception as e:
        return False, f"✗ Agent check failed: {e}"


def check_analytics() -> Tuple[bool, str]:
    """Check analytics system."""
    try:
        from src.analytics import PerformanceAnalyzer
        
        analyzer = PerformanceAnalyzer()
        
        # Record test episode
        metrics = {
            "final_score": 0.85,
            "priority_handling": 0.8,
            "response_speed": 0.9,
            "resource_usage": 0.85
        }
        
        env_stats = {
            "step_count": 10,
            "emergencies_handled": 2,
            "high_severity_handled": 1,
            "avg_response_time": 2.5,
            "unhandled_emergencies": 0
        }
        
        analyzer.add_episode(
            episode_number=1,
            task_difficulty="easy",
            agent_name="test",
            total_reward=0.85,
            metrics=metrics,
            env_stats=env_stats
        )
        
        # Check episodes were recorded
        if len(analyzer.episodes) == 0:
            return False, "✗ Analytics failed to record episode"
        
        return True, "✓ Analytics system operational"
    except Exception as e:
        return False, f"✗ Analytics check failed: {e}"


def check_curriculum_learning() -> Tuple[bool, str]:
    """Check curriculum learning works."""
    try:
        from src.training import CurriculumLearner
        from src.env import EmergencyResponseEnv
        from src.advanced_agents import create_agent
        
        curriculum = CurriculumLearner()
        env = EmergencyResponseEnv("easy")
        agent = create_agent(env, "adaptive")
        
        # Run few steps
        for _ in range(3):
            task = curriculum.get_next_task()
            env = EmergencyResponseEnv(task)
            state = env.reset()
            action = agent.get_action(state)
            next_state, reward, done, info = env.step(action)
            curriculum.record_score(task, 0.7)
        
        return True, "✓ Curriculum learning operational"
    except Exception as e:
        return False, f"✗ Curriculum learning check failed: {e}"


def main():
    """Run all validation checks."""
    print("╔" + "═" * 58 + "╗")
    print("║ EMERGENCY RESPONSE ENVIRONMENT - HACKATHON VALIDATION ║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    checks = [
        ("Imports", check_imports),
        ("OpenEnv Compliance", check_openenv_compliance),
        ("Environment Structure", check_environment_structure),
        ("Grading System", check_grading_system),
        ("Task Progression", check_task_progression),
        ("Inference Output", check_inference_output),
        ("Agent Types", check_agents),
        ("Analytics System", check_analytics),
        ("Curriculum Learning", check_curriculum_learning),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for name, check_func in checks:
        print(f"Checking {name}...", end=" ", flush=True)
        success, message = check_func()
        results.append((name, success, message))
        
        if success:
            print(message)
            passed += 1
        else:
            print(message)
            failed += 1
    
    # Summary
    print()
    print("╔" + "═" * 58 + "╗")
    print(f"║ VALIDATION SUMMARY: {passed} PASSED, {failed} FAILED" + " " * (58-30) + "║")
    print("╚" + "═" * 58 + "╝")
    
    if failed == 0:
        print()
        print("🎉 ALL CHECKS PASSED - READY FOR HACKATHON SUBMISSION!")
        return 0
    else:
        print()
        print(f"⚠️  {failed} CHECK(S) FAILED - PLEASE FIX BEFORE SUBMISSION")
        return 1


if __name__ == "__main__":
    sys.exit(main())
