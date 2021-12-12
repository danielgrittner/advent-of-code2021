import sys


START_NODE = 'start'
END_NODE = 'end'
VISITED = True
NOT_VISITED = False


def _read_input(path: str) -> dict:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()

    graph = {
        START_NODE: [],
        END_NODE: []
    }

    for edge in file_content:
        edge = edge[:-1].split('-')
        v1, v2 = edge[0], edge[1]
        
        if v1 not in graph:
            graph[v1] = []
        graph[v1].append(v2)        
        
        if v2 not in graph:
            graph[v2] = []
        graph[v2].append(v1)

    return graph


def _all_paths_dfs(node: str, graph: dict, small_caves: dict, single_sm_twice=False) -> int:
    if node == END_NODE:
        return 1

    num_found_paths = 0

    for next_node in graph[node]:
        if next_node.islower():
            # We have a small cave!
            if small_caves[next_node]:
                # We already visited it
                if single_sm_twice and next_node != START_NODE:
                    # Although we already visited it, we are allowed to visit it twice!
                    num_found_paths += _all_paths_dfs(next_node, graph, small_caves, single_sm_twice=False)
            else:
                # We did not yet visit it!
                small_caves[next_node] = VISITED
                num_found_paths += _all_paths_dfs(next_node, graph, small_caves, single_sm_twice=single_sm_twice)
                small_caves[next_node] = NOT_VISITED
        else:
            num_found_paths += _all_paths_dfs(next_node, graph, small_caves, single_sm_twice=single_sm_twice)

    return num_found_paths


def _get_small_caves_map(graph: dict) -> dict:
    small_caves = {}
    for node in graph.keys():
        if node.islower():
            small_caves[node] = NOT_VISITED
    small_caves[START_NODE] = VISITED
    return small_caves


def solve1(graph: dict) -> int:
    small_caves = _get_small_caves_map(graph)
    return _all_paths_dfs(START_NODE, graph, small_caves)


def solve2(graph: dict) -> int:
    small_caves = _get_small_caves_map(graph)
    return _all_paths_dfs(START_NODE, graph, small_caves, single_sm_twice=True)


if __name__ == "__main__":
    input_path = sys.argv[1]
    g = _read_input(input_path)
    print(solve1(g))
    print(solve2(g))