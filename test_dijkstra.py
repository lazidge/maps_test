from collections import defaultdict
from heapq import heappush, heappop, heapify
import math
from algorithms import HeapItem

def dijkstra(adjacency_list, source_id, target_id):
    shortest_path = []
    #paths = defaultdict(lambda: [])
    shortest_distance = float('Inf')
    queue = []
    heapify(queue)
    visited = set()
    shortest_distances = defaultdict(lambda: float('inf'))
    shortest_distances[source_id] = 0
    heappush(queue, (0, source_id, [source_id])) # (distance, node_id, path)
    shortest_distances[source_id] = 0
    while queue:
        dist1, node1, path1 = heappop(queue)
        if node1 == target_id:
            shortest_path = path1
            last = float('Inf')
            """for i in node:
                if i.distance < last:
                    last = i"""
            shortest_distance = dist1
            print("yeet")
            break
        elif not node1 in visited:
            visited.add(node1)
            #print(visited)
            #print(node)
            for neighbor, weight in adjacency_list[node1]:
                dist2 = dist1 + weight
                if dist2 < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = dist2
                    heappush(queue, (dist2, neighbor, path1 + [neighbor]))
                #print(shortest_distances[node.node_id])
    #print(shortest_distance)
    return shortest_distance, shortest_path

    """ To be implemented by students (optional exercise). `adjacency_list` is a dictionary with structure:
    {node_id: [...(neighbor_id, weight)]}.
    Function should return (distance, path). Path should be a list of the nodes in the shortest path
    **including** the source_id and target_id. If no shortest path is found, it should return (float('inf'), []) """

    return float('inf'), []


if __name__ == '__main__':
    file = open('data/dijkstra.test') # Feel free to add your own test cases to the file!
    testcase = 0
    try:
        while True:
            num_nodes = file.readline()
            if num_nodes[0] == '#':
                continue
            testcase += 1
            num_nodes = int(num_nodes)
            source, target = map(int, file.readline().split())
            nodes = []
            for n in range(num_nodes):
                x, y = map(float, file.readline().split())
                nodes.append((x, y))
            adjacency_list = defaultdict(list)
            num_edges = int(file.readline())
            for m in range(num_edges):
                v1, v2 = map(int, file.readline().split())
                x1, y1 = nodes[v1]
                x2, y2 = nodes[v2]
                weight = math.hypot(x2-x1, y2-y1) # Get distance between the nodes
                adjacency_list[v1].append((v2, weight))
                adjacency_list[v2].append((v1, weight))
            correct_dist = float(file.readline())
            correct_path = [int(v) for v in file.readline().split()]
            dist, path = dijkstra(adjacency_list, source, target)
            assert abs(correct_dist-dist) < 1e-3
            assert correct_path == path
            print("Passed test case {}".format(testcase))
    except AssertionError:
        print("Failed test case {}".format(testcase))
    except IndexError:
        print('Passed all test cases')
    except EOFError:
        print('Passed all test cases')
