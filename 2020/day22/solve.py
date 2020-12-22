def parse_input(data):
    return [list(map(int, p.strip().split('\n')[1:])) for p in data.split('\n\n')]


def play(p1, p2):
    while len(p1) != 0 and len(p2) != 0:
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        w = p1 if c1 > c2 else p2
        w.extend((c1, c2) if w is p1 else (c2, c1))
    return p1 or p2


def play_recursive(p1, p2):
    seen = set()
    while len(p1) != 0 and len(p2) != 0:
        h = hash((tuple(p1), tuple(p2)))
        if h in seen:
            return p1, 1
        seen.add(h)

        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if len(p1) >= c1 and len(p2) >= c2:
            _, rec_win = play_recursive(p1[:c1], p2[:c2])
            w = p1 if rec_win == 1 else p2
        else:
            w = p1 if c1 > c2 else p2
        w.extend((c1, c2) if w is p1 else (c2, c1))
    winner = p1 or p2
    return winner, (1 if winner is p1 else 2)


def calculate_score(player):
    return sum(c * m for c, m in zip(player, range(len(player), 0, -1)))


with open('input.txt', 'r') as f:
    data = f.read()

player1, player2 = parse_input(data)

# part 1
winner = play(player1.copy(), player2.copy())
print(calculate_score(winner))

# part 2
winner_rec, _ = play_recursive(player1.copy(), player2.copy())
print(calculate_score(winner_rec))
