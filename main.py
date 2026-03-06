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
    
def resolve_in_path(cmd: str, path_entries: list[str]) -> str | None:
    for directory in path_entries:
        if not directory:
            directory = "."
        candidate = os.path.join(directory, cmd)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def index_path(path_entries: list[str]) -> set[str]:
    commands: set[str] = set()

    for directory in path_entries:
        if not directory:
            directory = "."

        if not os.path.isdir(directory):
            continue

        try:
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)

                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    commands.add(entry)
        except PermissionError:
            continue

    return commands


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    if len(a) > len(b):
        a, b = b, a

    previous_row = list(range(len(a) + 1))

    for i, bc in enumerate(b, start=1):
        current_row = [i]
        for j, ac in enumerate(a, start=1):
            insert_cost = current_row[j - 1] + 1
            delete_cost = previous_row[j] + 1
            replace_cost = previous_row[j - 1] + (ac != bc)

            current_row.append(min(insert_cost, delete_cost, replace_cost))

        previous_row = current_row

    return previous_row[-1]



cmd = tokens[0]

if classify_command(cmd) == "BARE":
    path_entries = get_path_entries(path_string)
    resolved = resolve_in_path(cmd, path_entries)

    if resolved:
        print(resolved)
    else:
        print(f"lint: command {cmd} not found!")
        command_index = index_path(path_entries)
        print(f"indexed {len(command_index)} commands")

        


        

