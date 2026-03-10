import os, sys
from .resolver import get_path_entries, resolve_in_path, index_path
from .suggester import levenshtein as levenshtein_distance, suggest



def classify_command(cmd: str) -> str:
    if cmd.startswith("/") or cmd.startswith("./") or cmd.startswith("../"):
        return "PATH"
    return "BARE"

def main():
    invoke = sys.argv[0]
    tokens = sys.argv[1:]
    path_string = os.environ.get("PATH")

    if not tokens:
        print(f"Usage: {invoke} <tokens...>")
        sys.exit(1)

    for token in tokens:
        classification = classify_command(token)

        if classification == "PATH":
            resolved = token if os.path.isfile(token) and os.access(token, os.X_OK) else None
            if resolved:
                print(resolved)
            else:
                print(f"{invoke}: {token}: No such file or directory")
        elif classification == "BARE":
            path_entries = get_path_entries(path_string)
            resolved = resolve_in_path(token, path_entries)
            if resolved:
                print(resolved)
            else:
                command_index = index_path(path_entries)
                suggestion = suggest(token, command_index)
                if suggestion:
                    answer = input(f"{invoke}: {token}: command not found. Did you mean '{suggestion}'? [y/N] ").strip().lower()
                    if answer == "y":
                        full_path = resolve_in_path(suggestion, path_entries)
                        os.execv(full_path, [suggestion] + tokens[1:])
                else:
                    print(f"{invoke}: {token}: command not found.")
    



if __name__ == "__main__":
    main()