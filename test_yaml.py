#!/usr/bin/env python3
import os
import yaml

# Check if openenv.yaml exists
if os.path.exists('openenv.yaml'):
    print("✓ openenv.yaml exists at root")
    with open('openenv.yaml') as f:
        data = yaml.safe_load(f)
        print(f"✓ Version: {data.get('version')}")
        print(f"✓ Name: {data.get('name')}")
else:
    print("✗ openenv.yaml NOT found at root")

# Check git status
import subprocess
result = subprocess.run(['git', 'status', 'openenv.yaml'], capture_output=True, text=True)
print(f"\nGit status:\n{result.stdout}")
