#!/usr/bin/env python3
"""
Test script to demonstrate all improved error messages.
Run each command to see the helpful error messages in action.
"""

import subprocess
import sys
import os

os.chdir('c:\\Users\\030922\\Desktop\\Essadeq\\Copilot\\datagrep-cli')

test_cases = [
    {
        'name': 'WHERE condition without spaces',
        'command': 'python src/datagrep.py examples/data/sample_customers.csv name john --where "status==active"',
        'expected': 'Expected format: "column operator value"'
    },
    {
        'name': 'Invalid operator in WHERE',
        'command': 'python src/datagrep.py examples/data/sample_customers.csv name john --where "status ~~ active"',
        'expected': 'Valid operators are: ==, !=, >, <, >=, <=, contains, startswith, endswith'
    },
    {
        'name': 'Missing column in --columns',
        'command': 'python src/datagrep.py examples/data/sample_customers.csv --columns nonexistent name john',
        'expected': 'Available columns in this file:'
    },
    {
        'name': 'Non-existent file',
        'command': 'python src/datagrep.py nonexistent.csv name john',
        'expected': 'The file does not exist at that path'
    },
    {
        'name': 'Valid WHERE condition',
        'command': 'python src/datagrep.py examples/data/sample_customers.csv name john --where "city == London"',
        'expected': 'jane.doe@example.com'
    },
]

print("=" * 80)
print("IMPROVED ERROR MESSAGES TEST SUITE")
print("=" * 80)
print()

for i, test in enumerate(test_cases, 1):
    print(f"\n[Test {i}] {test['name']}")
    print("-" * 80)
    print(f"Command: {test['command']}")
    print(f"Expected to contain: '{test['expected']}'")
    print("\nOutput:")
    print("-" * 40)
    
    result = subprocess.run(test['command'], shell=True, capture_output=True, text=True)
    output = result.stderr + result.stdout
    
    if test['expected'] in output:
        print("✓ PASS - Found expected text in output")
    else:
        print("✗ FAIL - Expected text not found")
    
    print(output[:500])  # Show first 500 chars
    if len(output) > 500:
        print("... (output truncated)")

print("\n" + "=" * 80)
print("TEST SUITE COMPLETE")
print("=" * 80)
