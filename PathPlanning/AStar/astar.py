import matplotlib.pyplot as plt
from math import sqrt
import sys, os
import heapq



def euclidean_distance(point1, point2):
    """
    Euclidean distance heuristic to estimate the cost from a given point to the end point.
    """
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def intersect_obstacle(map_obj, start_point, end_point):
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles

    if (start_point[0] < 0 or start_point[0] >= x_range or
        start_point[1] < 0 or start_point[1] >= y_range or 
        start_point in obstacles or 
        end_point[0] < 0 or end_point[0] >= x_range or
        end_point[1] < 0 or end_point[1] >= y_range or
        end_point in obstacles):
        print("Start point and end point must not be in the obstacle!")
        return True
    return False


def draw_map(ax, map_obj, start_point, end_point, visited_points, path, current_point=None):
    ax.clear()
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles
    obstacles_lines = map_obj.obstacles_lines

    # Plot obstacles
    for obstacle in obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        ax.plot(x_coords, y_coords, color='black', linewidth=1)

    # Plot visited points
    for point in visited_points:
        ax.scatter(point[0], point[1], color='green', s=5)

    # Plot path
    for i in range(len(path) - 1):
        ax.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], color='red')


    # Plot current point
    if current_point:
        ax.scatter(current_point[0], current_point[1], color='green', s=50)

    # Plot start and end points
    ax.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
    ax.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')
 
    if(current_point==end_point):
        #ax.scatter(end_point[0], end_point[1], color='green', s=100, label='End Point')
        ax.plot([path[-1][0], end_point[0]], [path[-1][1], end_point[1]], color='red')
        
    ax.set_xlim(0, x_range)
    ax.set_ylim(0, y_range)
    ax.grid(True)
    plt.pause(0.001)

def astar(ax, map_obj, start_point, end_point, only_result):
    """
    A* algorithm to find the shortest path between two points on the map.
    :param ax: plot on axes
    :param map_obj: Map class object (EmptyMap, QuadraticMap, LineMap)
    :param start_point: Coordinates of the start point in the format (x, y)
    :param end_point: Coordinates of the end point in the format (x, y)
    :param only_result: Boolean, Draw only result (not step by step) if True
    :return: List of coordinates representing the shortest path from start_point to end_point.
    """
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles

    if intersect_obstacle(map_obj, start_point, end_point):
        return None

    pq = [(0 + euclidean_distance(start_point, end_point), 0, start_point, [])]  # Priority queue (heuristic + cost, cost, current_point, path)
    heapq.heapify(pq) 
    visited = set()
    shortest_cost = {}

    print("Starting A*...")
    while pq:
        _, cost, current_point, path = heapq.heappop(pq)  # Get the lowest priority item from the heap
        if only_result is False:
            draw_map(ax, map_obj, start_point, end_point, visited, path, current_point) # Uncomment to draw every node added to the tree
        visited.add(current_point)

        if current_point == end_point:
            print("Path found:", path + [current_point])
            path.append(end_point)
            draw_map(ax, map_obj, start_point, end_point, visited, path, current_point)
            return path

        neighbors = [(current_point[0] + dx, current_point[1] + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]]
        valid_neighbors = [n for n in neighbors if 0 <= n[0] < x_range and 0 <= n[1] < y_range and n not in obstacles]

        for neighbor in valid_neighbors:
            dx = abs(neighbor[0] - current_point[0])
            dy = abs(neighbor[1] - current_point[1])
            if dx == 1 and dy == 1:
                new_cost = cost + sqrt(2)
            else:
                new_cost = cost + 1

            if neighbor not in shortest_cost or new_cost < shortest_cost[neighbor]:
                shortest_cost[neighbor] = new_cost
                priority = new_cost + euclidean_distance(neighbor, end_point)
                heapq.heappush(pq, (priority, new_cost, neighbor, path + [current_point]))

    print("Path not found.")
    return None