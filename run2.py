import copy
import sys
from collections import deque, defaultdict


def can_isolate(graph: defaultdict, virus: str) -> tuple[str, bool]:
    free_moves = 0
    fs = ''

    def bfs_next_step(virus_pos: str) -> tuple[str, str, int]:
        visited = {virus_pos}
        parent = {virus_pos: None}
        q = deque([(virus_pos, 0)])
        met_gateway = False
        variants = []

        while q:
            node, current_dist = q.popleft()
            for nb in sorted(graph[node]):
                if nb in visited:
                    continue
                visited.add(nb)
                parent[nb] = node
                if nb[0].isupper():
                    met_gateway = True
                    penultimate = node
                    distance_to_gateway = current_dist + 1
                    first_step = penultimate
                    while parent[first_step] != virus_pos and parent[first_step] is not None:
                        first_step = parent[first_step]
                    variants.append((first_step, penultimate, distance_to_gateway, nb[0]))
                else:
                    q.append((nb, current_dist + 1))
        if met_gateway:
            minimal = min(variants, key=lambda x: (x[2], x[3]))
            return minimal[0], minimal[1], minimal[2]
        return None, None, None

    while True:
        new_fs, target_node, dist = bfs_next_step(virus)
        if not target_node:
            return fs, True
        if fs == '':
            fs = new_fs
        degree = sum(1 for node in graph[target_node] if node.isupper())
        free_moves += dist - degree - 1
        if free_moves < 0:
            return '', False

        virus = target_node
        gateways = [node for node in graph[target_node] if node.isupper()]
        for gateway in gateways:
            for node in graph[gateway]:
                graph[node].remove(gateway)
            graph[gateway] = set()


def solve(edges: list[tuple[str, str]]) -> list[str]:
    result = []
    virus_pos = 'a'

    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    transits = sorted([sorted(edge) for edge in edges if edge[0].isupper() or edge[1].isupper()])
    while transits:
        for transit in transits:
            new_graph = copy.deepcopy(graph)
            new_graph[transit[0]].remove(transit[1])
            new_graph[transit[1]].remove(transit[0])
            new_virus_pos, can = can_isolate(new_graph, virus_pos)
            if can:
                result.append(transit[0] + '-' + transit[1])
                transits.remove(transit)
                virus_pos = new_virus_pos
                graph[transit[0]].remove(transit[1])
                graph[transit[1]].remove(transit[0])
                break

    return result
def test():
    edges = [('a', 'b'), ('b', 'c'), ('c', 'G'), ('b', 'f'), ('f', 'g'),
             ('b', 'd'), ('d', 'e'), ('e', 'C'), ('e', 'D'), ('e', 'E'), ('e', 'F'),
             ('g', 'A'), ('g', 'B'), ('e', 'H')]
    result = solve(edges)
    for edge in result:
        print(edge)

def main():
    test()
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)

if __name__ == "__main__":
    main()
