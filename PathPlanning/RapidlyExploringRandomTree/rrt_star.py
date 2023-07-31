import matplotlib.pyplot as plt
import random
import sys
from math import sqrt

def draw_map(ax, map_obj, start_point, end_point, nodes, path=None):
    ax.clear()
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines

    # Plot obstacles
    for obstacle in obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        ax.plot(x_coords, y_coords, color='black', linewidth=1)

    # Plot nodes
    for node, parent_node,_ in nodes:
        #plt.scatter(node[0], node[1], color='gray', s=5)
        if parent_node is not None and node != end_point:
            ax.plot([node[0], parent_node[0]], [node[1], parent_node[1]], color='green', alpha=0.5)

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


def rrt_star(ax, map_obj, start_point, end_point, only_result, max_points=10000, rewire_radius=5.0):
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines
    nodes = [(start_point, None, 0)] 
    parent_nodes = {start_point: None}
    costs = {start_point: 0}

    if (start_point[0] < 0 or start_point[0] >= x_range or
        start_point[1] < 0 or start_point[1] >= y_range or 
        start_point in obstacles or 
        end_point[0] < 0 or end_point[0] >= x_range or
        end_point[1] < 0 or end_point[1] >= y_range or
        end_point in obstacles):
        print("Start point and end point must not be in the obstacle!")
        return None

    print("Starting RRT*...")
    points_added = 0
    while points_added < max_points:
        # 1. Draw a point
        target_point = (round(random.uniform(0, x_range), 2), round(random.uniform(0, y_range), 2))

        if is_far_from_obstacles(target_point, obstacles):
            # 2. Checking for each available node (parent).
            nearest_node = None
            min_cost = float('inf')
            for node, parent_node, cost in nodes:
                if not intersects_obstacle(node, target_point, obstacles_lines):
                    # 2a. Calculating the cost from the beginning of the route to this point by this parent.
                    new_cost = costs[node] + euclidean_distance(node, target_point)
                    if new_cost < min_cost:
                        nearest_node = node
                        min_cost = new_cost
        
        if nearest_node is not None:
                # 2b. Selecting the shortest distance to the starting point and saving the point to that parent.
                nodes.append((target_point, nearest_node, min_cost))
                parent_nodes[target_point] = nearest_node
                costs[target_point] = min_cost

                # 3. Selecting the parent with the lowest cost.
                for node, parent_node, cost in nodes:
                    if node != target_point and euclidean_distance(node, target_point) <= rewire_radius:
                        new_cost = costs[target_point] + euclidean_distance(node, target_point)
                        if new_cost < costs[node] and not intersects_obstacle(node, target_point, obstacles_lines):
                            parent_nodes[node] = target_point
                            costs[node] = new_cost

                points_added += 1
                if only_result is False:
                    draw_map(ax, map_obj,start_point, end_point, nodes) # Draw added nodes

                # 4: Checking whether a point can be connected to an endpoint
                if euclidean_distance(target_point, end_point) <= 5.0 and not intersects_obstacle(end_point, target_point, obstacles_lines):
                    
                    nodes.append((end_point, target_point, min_cost + euclidean_distance(target_point, end_point)))
                    parent_nodes[end_point] = target_point
                    costs[end_point] = min_cost + euclidean_distance(target_point, end_point)

                    # Create final path
                    path = [end_point]
                    current_node = target_point
                    while current_node != start_point:
                        path.append(current_node)
                        current_node = parent_nodes[current_node]
                    path.append(start_point)
                    path.reverse()
                    draw_map(map_obj, start_point, end_point, nodes, path)
                    print("Path found at", points_added, "iteration.")
                    print("Path:", path)
                    return path

    print("Path not found.")
    return None
