"""
Simple test to verify environment works correctly.

Run with: python tests/test_env.py
"""

import sys
sys.path.insert(0, '.')

from src.env import EmergencyResponseEnv
from src.graders import create_grader_for_task


def test_environment_reset():
    """Test environment initialization."""
    print("Testing environment reset...")
    env = EmergencyResponseEnv(task_difficulty="easy")
    state = env.reset()
    
    assert "emergencies" in state
    assert "ambulances" in state
    assert "hospitals" in state
    assert "traffic_level" in state
    print("✓ Reset works correctly")


def test_step_execution():
    """Test step execution."""
    print("Testing step execution...")
    env = EmergencyResponseEnv(task_difficulty="easy")
    state = env.reset()
    
    # Get available options
    available_ambulances = [a["id"] for a in state["ambulances"] if a["available"]]
    unassigned_emergencies = [e["id"] for e in state["emergencies"] if not e["assigned"]]
    available_hospitals = [h["id"] for h in state["hospitals"] if h["capacity"] > 0]
    
    if available_ambulances and unassigned_emergencies and available_hospitals:
        action = {
            "ambulance_id": available_ambulances[0],
            "emergency_id": unassigned_emergencies[0],
            "hospital_id": available_hospitals[0]
        }
        
        next_state, reward, done, info = env.step(action)
        
        assert isinstance(reward, float)
        assert isinstance(done, bool)
        assert "valid_action" in info
        print(f"✓ Step executed successfully (reward: {reward:.3f})")


def test_task_difficulties():
    """Test different task difficulties."""
    print("Testing task difficulties...")
    
    for difficulty in ["easy", "medium", "hard"]:
        env = EmergencyResponseEnv(task_difficulty=difficulty)
        state = env.reset()
        
        num_emergencies = len(state["emergencies"])
        available_ambulances = sum(1 for a in state["ambulances"] if a["available"])
        
        print(f"  {difficulty.upper()}: {num_emergencies} emergencies, {available_ambulances} ambulances available")
    
    print("✓ All task difficulties work")


def test_grader():
    """Test grading system."""
    print("Testing grader...")
    
    env = EmergencyResponseEnv(task_difficulty="easy")
    grader = create_grader_for_task("easy")
    
    state = env.reset()
    step_history = []
    
    # Run a few steps
    for _ in range(5):
        action = {
            "ambulance_id": 1,
            "emergency_id": 1,
            "hospital_id": 1
        }
        next_state, reward, done, info = env.step(action)
        step_history.append((state, action, reward, done))
        state = next_state
        
        if done:
            break
    
    metrics = grader.evaluate_episode(env, step_history)
    
    assert "final_score" in metrics
    assert 0.0 <= metrics["final_score"] <= 1.0
    print(f"✓ Grader works (score: {metrics['final_score']:.3f})")


if __name__ == "__main__":
    print("=" * 60)
    print("Emergency Response Environment - Quick Tests")
    print("=" * 60 + "\n")
    
    try:
        test_environment_reset()
        test_step_execution()
        test_task_difficulties()
        test_grader()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
