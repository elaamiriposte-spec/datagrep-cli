import sys
import traceback

sys.argv = ['datagrep', 'examples/data/sample_customers.csv', 'status', 'active', '--limit', '3']

from src.cli import main

try:
    main()
except Exception as e:
    with open('error_trace.txt', 'w') as f:
        traceback.print_exc(file=f)
    print(f"Error written to error_trace.txt")
