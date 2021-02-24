import math
from heapq import heapify, heappop, heappush
from collections import defaultdict
from store import Node

def length_haversine(p1, p2):
    lat1 = p1.lat
    lng1 = p1.lng
    lat2 = p2.lat
    lng2 = p2.lng
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2) ** 2 +\
    math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return 6372797.560856 * c # return the distance in meters


def check_tile(offset, tiles, lng, lat):
    """
    Checks 'tiles' for a given coordinate
    """
    lat = float(lat)
    lng = float(lng)
    x_coordinate = lat + offset[0]
    y_coordinate = lng + offset[1]
    x_coordinate = format(x_coordinate, '.3f')
    y_coordinate = format(y_coordinate, '.3f')
    print("x:", x_coordinate, "    y:", y_coordinate)
    key = (x_coordinate, y_coordinate)
    print("key: ", key)
    if not tiles[(key)]:
        return [False]
    else:
        print("yay")
        return [True, str(x_coordinate), str(y_coordinate)]


def get_closest_node_id(nodes, tiles, source_node):
    """ Search through all nodes and return the id of the node
    that is closest to 'source_node'. """
    shortest_distance = float('Inf')
    closest_node_id = 0
    this_lat = format(source_node.lat, '.3f')
    this_lng = format(source_node.lng, '.3f')
    visited = set()
    offset = 1
    print((this_lat, this_lng))
    while not tiles[(this_lat, this_lng)]:
        for i in range(-1 * offset, offset):
            for j in range(-1 * offset, offset):
                temp = check_tile((i/1000, j/1000), tiles, this_lng, this_lat)
                if (i, j) in visited:
                    break
                visited.add((i, j))
                if temp[0]:
                    this_lat = temp[1]
                    this_lng = temp[2]
                    break
        offset += 1
    for node in tiles[(this_lat, this_lng)]:
        if length_haversine(nodes[str(node)], source_node) <= shortest_distance:
            shortest_distance = length_haversine(nodes[str(node)], source_node)
            closest_node_id = node
    return closest_node_id


class HeapItem:
    def __init__(self, node_id, distance, path, lat, lng, target_node):
        self.target_node = target_node
        self.lat = lat
        self.lng = lng
        self.node_id = node_id
        self.distance = distance
        self.path = path
    def __lt__(self, other_heap_item):
        return self.distance + length_haversine(self, self.target_node) <\
        other_heap_item.distance + \
        length_haversine(other_heap_item, self.target_node)


def find_shortest_path(nodes, source_id, target_id):
    """ Return the shortest path using A* """
    shortest_path = []
    shortest_distance = float('Inf')
    queue = []
    heapify(queue)
    visited = set()
    shortest_distances = defaultdict(lambda: float('inf'))
    shortest_distances[source_id] = 0
    heappush(queue, HeapItem(source_id, 0, [source_id],\
    nodes[str(source_id)].lat, nodes[str(source_id)].lng,\
    nodes[str(target_id)]))
    shortest_distances[source_id] = 0
    while queue:
        node = heappop(queue)
        if str(node.node_id) == str(target_id):
            node.path.append(node.node_id)
            shortest_path = node.path
            shortest_distance = shortest_distances[node.node_id]
            print("yeet")
            break
        elif not node.node_id in visited:
            visited.add(node.node_id)
            for neighbor in nodes[str(node.node_id)].neighbors:
                total_distance = shortest_distances[node.node_id] + \
                abs(length_haversine(nodes[str(node.node_id)], \
                nodes[str(neighbor)]))
                if total_distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = total_distance
                    neighbor_path = node.path.copy()
                    neighbor_path.append(neighbor)
                    heappush(queue, HeapItem(neighbor,\
                    shortest_distances[neighbor],\
                    neighbor_path,\
                    nodes[str(neighbor)].lat,\
                    nodes[str(neighbor)].lng,\
                    nodes[str(target_id)]))

    return shortest_path
