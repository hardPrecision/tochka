import sys
import heapq

ROOM_POS = [2, 4, 6, 8]
HALL_STOP = [0, 1, 3, 5, 7, 9, 10]
COST = [1, 10, 100, 1000]


def parse_input(lines):
    hallway = list(lines[1][1:-1])
    rooms = []
    depth = len(lines) - 3

    for i in range(4):
        col = 3 + 2 * i
        room = []
        for d in range(2, 2 + depth):
            room.append(lines[d][col])
        rooms.append(tuple(room))
    return tuple(hallway), tuple(rooms), depth


def is_organized(rooms):
    for i, room in enumerate(rooms):
        if any(c != chr(ord('A') + i) for c in room):
            return False
    return True


def path_clear(hallway, start, end):
    if start < end:
        rng = range(start + 1, end + 1)
    else:
        rng = range(end, start)
    return all(hallway[i] == '.' for i in rng)


def heuristic(hallway, rooms):
    h = 0
    for i, c in enumerate(hallway):
        if c != '.':
            target = ROOM_POS[ord(c) - ord('A')]
            h += abs(i - target) * COST[ord(c) - ord('A')]
    for room_index, room in enumerate(rooms):
        target_type = chr(ord('A') + room_index)
        for depth_index, c in enumerate(room):
            if c == '.':
                continue
            if c != target_type:
                from_pos = ROOM_POS[room_index]
                to_pos = ROOM_POS[ord(c) - ord('A')]
                h += (depth_index + 1 + abs(from_pos - to_pos) + 1) * COST[ord(c) - ord('A')]
    return h


def possible_moves(hallway, rooms):
    for i, c in enumerate(hallway):
        if c == '.':
            continue
        target_room_index = ord(c) - ord('A')
        target_room_pos = ROOM_POS[target_room_index]
        target_room_content = rooms[target_room_index]

        if path_clear(hallway, i, target_room_pos) and all(
                x in ('.', c) for x in target_room_content
        ):
            for j in range(len(target_room_content) - 1, -1, -1):
                if target_room_content[j] == '.':
                    d = j
                    break
            steps = abs(i - target_room_pos) + d + 1
            energy = steps * COST[ord(c) - ord('A')]

            new_hallway = list(hallway)
            new_hallway[i] = '.'
            new_rooms = [list(r) for r in rooms]
            new_rooms[target_room_index][d] = c

            yield tuple(new_hallway), tuple(tuple(r) for r in new_rooms), energy

    for room_index, room in enumerate(rooms):
        room_pos = ROOM_POS[room_index]
        for depth_index, c in enumerate(room):
            if c != '.':
                if all(x == chr(ord('A') + room_index) for x in room[depth_index:]):
                    break
                for direction in [-1, 1]:
                    pos = room_pos
                    while True:
                        pos += direction
                        if pos < 0 or pos > 10:
                            break
                        if hallway[pos] != '.':
                            break
                        if pos in HALL_STOP:
                            steps = abs(pos - room_pos) + depth_index + 1
                            energy = steps * COST[ord(c) - ord('A')]

                            new_hallway = list(hallway)
                            new_hallway[pos] = c
                            new_rooms = [list(r) for r in rooms]
                            new_rooms[room_index][depth_index] = '.'

                            yield tuple(new_hallway), tuple(tuple(r) for r in new_rooms), energy
                break


def solve(lines: list[str]) -> int:
    hallway, rooms, depth = parse_input(lines)
    start = (hallway, rooms)
    pq = [(heuristic(hallway, rooms), 0, start)]
    best = {start: 0}

    while pq:
        _, cost, (hallway, rooms) = heapq.heappop(pq)
        if is_organized(rooms):
            return cost
        if cost > best[(hallway, rooms)]:
            continue
        for nh, nr, step_cost in possible_moves(hallway, rooms):
            new_cost = cost + step_cost
            state = (nh, nr)
            if new_cost < best.get(state, float('inf')):
                best[state] = new_cost
                heapq.heappush(pq, (new_cost + heuristic(nh, nr), new_cost, state))
    return -1


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()