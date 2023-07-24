import matplotlib.pyplot as plt
import random
import sys
from math import sqrt
sys.path.append('Maps')
from map_1 import QuadraticMap
from map_2 import LineMap
from empty_map import EmptyMap
from maze_1 import Maze1

def draw_map(map_obj, nodes, path=None):
    plt.clf() 
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines

    # Plot obstacles
    for obstacle in obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        plt.plot(x_coords, y_coords, color='black', linewidth=5)

    # Plot nodes
    for node, parent_node,_ in nodes:
        #plt.scatter(node[0], node[1], color='gray', s=5)
        if parent_node is not None and node != end_point:
            plt.plot([node[0], parent_node[0]], [node[1], parent_node[1]], color='green')

    # Plot start and end points
    plt.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
    plt.scatter(end_point[0], end_point[1], color='red', s=100, label='End Point')

    # Plot path
    if path:
        current_node = path[0]
        for next_node in path[1:]:
            plt.plot([current_node[0], next_node[0]], [current_node[1], next_node[1]], color='cyan')
            current_node = next_node
        plt.scatter(end_point[0], end_point[1], color='green', s=100, label='End Point')


        
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

def rrt_star(map_obj, start_point, end_point, max_iterations=100000):
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    nodes = [(start_point, None, 0)]  # Dodajemy koszt do węzła
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
    for _ in range(max_iterations):
        target_point = (round(random.uniform(0, x_range), 2), round(random.uniform(0, y_range), 2))
        
        nearest_dist = float('inf')
        nearest_node = None
        for node, parent, cost in nodes:
            dist = euclidean_distance(node, target_point)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_node = node
                nearest_parent = parent
                nearest_cost = cost
        
        if nearest_node is None:
            continue
                
        if nearest_dist >= 0.5 and nearest_dist <= 1.0 and is_far_from_obstacles(target_point, obstacles):
            parent = nearest_node if nearest_dist <= 1.0 else nearest_parent
            cost = nearest_cost + euclidean_distance(parent, target_point)
            
            current_node = nearest_node
            while current_node != start_point:
                if cost < costs[current_node]: 
                    costs[current_node] = cost
                    parent_nodes[current_node] = parent
                current_node = parent_nodes[current_node]
                
            nodes.append((target_point, parent, cost))
            parent_nodes[target_point] = parent
            costs[target_point] = cost
            #draw_map(map_obj, nodes)
            if euclidean_distance(target_point, end_point) <= 0.5 and is_far_from_obstacles(target_point, obstacles):
                nodes.append((end_point, target_point, cost + euclidean_distance(target_point, end_point)))
                parent_nodes[end_point] = target_point
                costs[end_point] = cost + euclidean_distance(target_point, end_point)
                #print("PARENT NODES", parent_nodes)
                print("Path found.")
                path = [end_point]
                current_node = target_point
                while current_node != start_point:
                    path.append(current_node)
                    current_node = parent_nodes[current_node]
                path.append(start_point)
                path.reverse()
                draw_map(map_obj, nodes, path)
                print("path: ", path)
                return path
    print("Path not found.")
    return None

if __name__ == "__main__":
    """
    Available map:
    -QuadraticMap()
    -LineMap()
    -EmptyMap()
    -Maze1()
    """    
    map = QuadraticMap()
    start_point = (1, 1)
    end_point = (9, 9)
    rrt_star(map, start_point, end_point)
    plt.show()
