



def suggest(cmd: str, command_index: set[str]) -> str | None:
    if not command_index:
        return None
    best = min(command_index, key=lambda c: levenshtein(cmd, c))
    distance = levenshtein(cmd, best)
    return best if distance <= 3 else None

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