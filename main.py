import sys



invoke = sys.argv[0]
tokens = sys.argv[1:]

if not tokens:
    print(f"Usage: {invoke} <tokens...>")
    sys.exit(1)
