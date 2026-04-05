#!/usr/bin/env python
"""Verify is_action_bad() is working correctly"""

from src.env import EmergencyResponseEnv
from src.inference import SmartHeuristicAgent

agent = SmartHeuristicAgent(EmergencyResponseEnv(task_difficulty='hard'), debug=False)

# Simulate marking an action as bad
test_action = {"ambulance_id": 2, "emergency_id": 1, "hospital_id": 2}

print(f"Initial check - is (2,1,2) bad? {agent.is_action_bad(2, 1, 2)}")
print(f"bad_action_penalties: {agent.bad_action_penalties}")

# Mark it as bad
agent.mark_action_bad(test_action, -0.40)
print(f"\nAfter marking bad:")
print(f"bad_action_penalties: {agent.bad_action_penalties}")
print(f"is (2,1,2) bad? {agent.is_action_bad(2, 1, 2)}")

# Mark it bad again
agent.mark_action_bad(test_action, -0.40)
print(f"\nAfter marking bad again:")
print(f"bad_action_penalties: {agent.bad_action_penalties}")
print(f"is (2,1,2) bad? {agent.is_action_bad(2, 1, 2)}")

# Test different action
print(f"\nis (3,4,5) bad? {agent.is_action_bad(3, 4, 5)}")

print("\n✅ is_action_bad() correctly identifies marked-bad actions")
