#!/usr/bin/env python
"""Check if is_action_bad is using the updated code"""

from src.inference import SmartHeuristicAgent
import inspect

source = inspect.getsource(SmartHeuristicAgent.is_action_bad)
if "bad_action_penalties.get" in source:
    print("✅ UPDATED: is_action_bad is checking bad_action_penalties directly")
else:
    print("❌ OLD: is_action_bad is still using the deque")

print("\nActual source:")
print(source)
