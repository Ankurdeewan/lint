import os

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