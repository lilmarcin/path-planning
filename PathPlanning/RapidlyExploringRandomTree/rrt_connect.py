import matplotlib.pyplot as plt
import random
import sys
from math import sqrt

def draw_map(ax, map_obj, start_point, end_point, start_nodes, end_nodes, path=None):
    ax.clear()
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines

    # Plot obstacles
    for obstacle in obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        ax.plot(x_coords, y_coords, color='black', linewidth=1)

    # Plot nodes from start tree
    for node, parent_node in start_nodes:
        if parent_node is not None and node != end_point:
            ax.plot([node[0], parent_node[0]], [node[1], parent_node[1]], color='blue', alpha=0.25)

    # Plot nodes from end tree
    for node, parent_node in end_nodes:
        if parent_node is not None and node != start_point:
            ax.plot([node[0], parent_node[0]], [node[1], parent_node[1]], color='teal', alpha=0.25)


    # Plot start and end points
    ax.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
    ax.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')

    # Plot path
    if path:
        current_node = path[0]
        for next_node in path[1:]:
            ax.plot([current_node[0], next_node[0]], [current_node[1], next_node[1]], color='red')
            current_node = next_node
        
    ax.set_xlim(0, x_range)
    ax.set_ylim(0, y_range)
    ax.grid(True)
    plt.pause(0.001)

def euclidean_distance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def is_far_from_obstacles(point, obstacles, min_distance=0.5):
    """
    Checks if the drawn point is at least in min_distance from obstacles.
    """
    for obstacle in obstacles:
        if euclidean_distance(point, obstacle) < min_distance:
            return False
    return True

def intersects_obstacle(point1, point2, obstacles_lines):
    for obstacle in obstacles_lines:
        for i in range(len(obstacle)):
            x1, y1 = obstacle[i]
            x2, y2 = obstacle[(i + 1) % len(obstacle)]
            if check_segments_intersect(point1, point2, (x1, y1), (x2, y2)):
                return True
    return False

def check_segments_intersect(p1, q1, p2, q2):
    # Sprawdzamy czy odcinek (point1, point2) przecina odcinek (x1, y1) -> (x2, y2)
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def on_segment(p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2 and o3 != o4) or (o1 == 0 and on_segment(p1, p2, q1)) or \
            (o2 == 0 and on_segment(p1, q2, q1)) or \
            (o3 == 0 and on_segment(p2, p1, q2)) or \
            (o4 == 0 and on_segment(p2, q1, q2)):
        return True
    return False



def rrt_connect(ax, map_obj, start_point, end_point, only_result, max_points=10000):
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines

    def add_node(node, parent, nodes, parent_nodes):
        nodes.append((node, parent))
        parent_nodes[node] = parent
        if only_result is False:
            draw_map(ax, map_obj, start_point, end_point, start_nodes, end_nodes) # Uncomment to draw every node to the tree

    def extend_tree(target_point, nodes, parent_nodes):
        nearest_dist = float('inf')
        nearest_node = None
        for node, parent in nodes:
            dist = euclidean_distance(node, target_point)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_node = node
                nearest_parent = parent

        if nearest_node is None:
            return False

        if nearest_dist <= 2.0 and is_far_from_obstacles(target_point, obstacles) and not intersects_obstacle(nearest_node, target_point, obstacles_lines):
            parent = nearest_node if nearest_dist <= 2.0 else nearest_parent
            add_node(target_point, parent, nodes, parent_nodes)
            return True

        return False

    def connect_trees(map_obj, start_nodes, end_nodes, start_parent_nodes, end_parent_nodes):
        if start_point == end_point:
            return [start_point]

        for start_node, start_parent in start_nodes:
            #print("Start node", start_node)
            for end_node, end_parent in end_nodes:
                #print("End node", end_node)
                if is_far_from_obstacles(end_node, obstacles) and not intersects_obstacle(start_node, end_node, obstacles_lines):
                    # Add the connecting node to both trees
                    start_parent_nodes[end_node] = start_node
                    end_parent_nodes[end_node] = end_parent
                    start_nodes.append((end_node, start_node))
                    end_nodes.append((end_node, end_parent))
                    #draw_map(map_obj, start_nodes, end_nodes)
                    print(f"Path found at {points_added} iteration.")
                    # Reconstruct the path
                    start_path = []
                    current_node = end_node
                    while current_node and current_node != start_point and current_node in start_parent_nodes:
                        start_path.append(current_node)
                        current_node = start_parent_nodes[current_node]
                    start_path.append(start_point)  # Add the starting point to the path
                    start_path.reverse()
                    #print("START PATH", start_path)
                    # Reconstruct path from common node to end
                    end_path = []
                    current_node = end_node
                    #print("CURRENT NODE", current_node)
                    while current_node and current_node != end_point and current_node in end_parent_nodes:
                        end_path.append(current_node)
                        current_node = end_parent_nodes[current_node]
                    end_path.append(end_point)
                    # Combine both paths
                    #print("END PATH", end_path)
                    path = start_path + end_path[1:]  # Avoid adding the common node twice
                    print("PATH", path)
                    # print("start_parent_nodes ", start_parent_nodes)
                    # print("start nodes ", start_nodes)
                    #print("end nodes", end_nodes)
                    #print("end_parent_nodes", end_parent_nodes)
                    draw_map(ax, map_obj, start_point, end_point, start_nodes, end_nodes, path)
                    return path

        return None


    if (start_point[0] < 0 or start_point[0] >= x_range or
        start_point[1] < 0 or start_point[1] >= y_range or 
        start_point in obstacles or 
        end_point[0] < 0 or end_point[0] >= x_range or
        end_point[1] < 0 or end_point[1] >= y_range or
        end_point in obstacles):
        print("Start point and end point must not be in the obstacle!")
        return None

    print("Starting RRT-Connect...")
    start_nodes = [(start_point, None)]
    end_nodes = [(end_point, None)]
    start_parent_nodes = {start_point: None}
    end_parent_nodes = {end_point: None}

    points_added = 0

    while points_added < max_points:
        target_point = (round(random.uniform(0, x_range), 2), round(random.uniform(0, y_range), 2))
        if extend_tree(target_point, start_nodes, start_parent_nodes):
            points_added += 1

        target_point = (round(random.uniform(0, x_range), 2), round(random.uniform(0, y_range), 2))
        if extend_tree(target_point, end_nodes, end_parent_nodes):
            points_added += 1
        #draw_map(map_obj, start_nodes, end_nodes) # Visualize every added point to the trees
        if points_added > 1:
            # Check for connecting paths between trees
            if connect_trees(map_obj, start_nodes, end_nodes, start_parent_nodes, end_parent_nodes):
                return None
            

    print("Path not found.")
    draw_map(map_obj, start_nodes, end_nodes)
    return None