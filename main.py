import sys
import os


invoke = sys.argv[0]
tokens = sys.argv[1:]
path_string = os.environ.get("PATH")

if not tokens:
    print(f"Usage: {invoke} <tokens...>")
    sys.exit(1)

def classify_command(cmd: str) -> str:
    if cmd.startswith("/") or cmd.startswith("./") or cmd.startswith("../"):
        return "PATH"
    return "BARE"

def get_path_entries(path_string: str) -> list[str]:
    if not path_string:
        return[]
    return path_string.split(":")

def resolve_bare_command(cmd: str, path_entries: list[str]) -> str | None:
    for directory in path_entries:
        candidate = os.path.join(directory, cmd)

        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    return None


if (classify_command(tokens[0]) == "BARE"):
    resolved = resolve_bare_command(tokens[0], get_path_entries(path_string))
    if resolved:
        print(resolved)
    else:
        print(f"lint: command {tokens[0]} not found!")
        

