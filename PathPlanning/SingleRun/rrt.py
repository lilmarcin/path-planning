import matplotlib.pyplot as plt
import random
import sys
from math import sqrt
sys.path.append('Maps')
from map_1 import QuadraticMap
from map_2 import LineMap
from empty_map import EmptyMap
from maze_1 import Maze1

def draw_map(map_obj,start_point, end_point, nodes, path=None):
    plt.clf() 
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines

    # Plot obstacles
    for obstacle in obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        plt.plot(x_coords, y_coords, color='black', linewidth=1)

    # Plot nodes
    for node, parent_node in nodes:
        #plt.scatter(node[0], node[1], color='gray', s=5)
        if parent_node is not None and node != end_point:
            plt.plot([node[0], parent_node[0]], [node[1], parent_node[1]], color='green', alpha=0.5)

    # Plot start and end points
    plt.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
    plt.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')

    # Plot path
    if path:
        current_node = path[0]
        for next_node in path[1:]:
            plt.plot([current_node[0], next_node[0]], [current_node[1], next_node[1]], color='red')
            current_node = next_node


        
    plt.xlim(0, x_range)
    plt.ylim(0, y_range)
    plt.grid(True)
    plt.pause(0.001)
    plt.draw()

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
    # Check if the segment (point1, point2) intersects the segment (x1, y1) -> (x2, y2)
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

def rrt(map_obj, start_point, end_point, max_points=10000):
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines
    nodes = [(start_point, None)]
    parent_nodes = {start_point: None}

    if (start_point[0] < 0 or start_point[0] >= x_range or
        start_point[1] < 0 or start_point[1] >= y_range or 
        start_point in obstacles or 
        end_point[0] < 0 or end_point[0] >= x_range or
        end_point[1] < 0 or end_point[1] >= y_range or
        end_point in obstacles):
        print("Start point and end point must not be in the obstacle!")
        return None

    print("Starting RRT...")
    points_added = 0
    while points_added < max_points:
        target_point = (round(random.uniform(0, x_range), 2), round(random.uniform(0, y_range), 2))
        #print("target point:", target_point)
        # Check that the point is at the correct distance from the nearest node
        nearest_dist = float('inf')
        nearest_node = None
        for node, parent in nodes:
            #print("node: ", node)
            dist = euclidean_distance(node, target_point)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_node = node
                nearest_parent = parent
        
        if nearest_node is None:
            continue
                
        if nearest_dist <= 0.5 and is_far_from_obstacles(target_point, obstacles):
            parent = nearest_node if nearest_dist <= 1.0 else nearest_parent
            if not intersects_obstacle(parent, target_point, obstacles_lines):
                current_node = nearest_node
                current_node = parent_nodes[current_node]
                nodes.append((target_point, parent))
                parent_nodes[target_point] = parent
                points_added += 1
                #draw_map(map_obj, nodes) # Uncomment to draw every node added to the tree
                
                if euclidean_distance(target_point, end_point) <= 1.0 and is_far_from_obstacles(target_point, obstacles):
                    nodes.append((end_point, target_point))
                    parent_nodes[end_point] = target_point
                    #print("PARENT NODES", parent_nodes)
                    print(f"Path found at {points_added} iteration.")
                    path = [end_point]
                    current_node = target_point
                    while current_node != start_point:
                        #print("PATH", path)
                        path.append(current_node)
                        current_node = parent_nodes[current_node] # Move to the parent of node
                    path.append(start_point)
                    path.reverse()
                    draw_map(map_obj, nodes, path) # Draw the final path
                    print("path: ", path)
                    return path
    print("Path not found.")
    draw_map(map_obj, nodes)
    return None

if __name__ == "__main__":
    """
    Available map:
    -QuadraticMap()
    -LineMap()
    -EmptyMap()
    -Maze1()
    """    
    map = Maze1()
    start_point = (5, 5)
    end_point = (5, 9)
    rrt(map, start_point, end_point)
    plt.show()
