import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from math import sqrt
import sys
import heapq
sys.path.append('Maps')
from map_1 import QuadraticMap
from map_2 import LineMap
from empty_map import EmptyMap
from maze_1 import Maze1

def euclidean_distance(point1, point2):
    """
    Euclidean distance heuristic to estimate the cost from a given point to the end point.
    """
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def draw_map(map_obj, visited_points, path, current_point=None):
    plt.clf() 
    x_range = map_obj.x_range
    y_range = map_obj.y_range
    obstacles = map_obj.obstacles

    # Plot obstacles
    for obstacle in obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='black', s=100)

    # Plot visited points
    for point in visited_points:
        plt.scatter(point[0], point[1], color='gray', s=50)

    # Plot path
    for i in range(len(path) - 1):
        plt.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], color='cyan')


    # Plot current point
    if current_point:
        plt.scatter(current_point[0], current_point[1], color='green', s=50)

    # Plot start and end points
    plt.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
    plt.scatter(end_point[0], end_point[1], color='red', s=100, label='End Point')

    if(current_point==end_point):
        plt.scatter(end_point[0], end_point[1], color='green', s=100, label='End Point')
        plt.plot([path[-1][0], end_point[0]], [path[-1][1], end_point[1]], color='cyan')
        
    plt.xlim(0, x_range)
    plt.ylim(0, y_range)
    plt.grid(True)
    plt.pause(0.001)


def astar(map_obj, start_point, end_point):
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
        return None

    pq = [(0 + euclidean_distance(start_point, end_point), 0, start_point, [])]  # Priority queue (heuristic + cost, cost, current_point, path)
    heapq.heapify(pq) 
    visited = set()
    shortest_cost = {}

    print("Starting A*...")
    while pq:
        _, cost, current_point, path = heapq.heappop(pq)  # Get the lowest priority item from the heap
        draw_map(map_obj, visited, path, current_point) 
        visited.add(current_point)

        if current_point == end_point:
            print("Path found:", path + [current_point])
            path.append(end_point)
            #draw_map(map_obj, visited, path, current_point)
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

if __name__ == "__main__":
    """
    Available map:
    -QuadraticMap()
    -LineMap()
    -EmptyMap()
    -Maze1()
    """    
    map = LineMap()
    start_point = (1, 1)
    end_point = (9, 9)
    # Wywołaj algorytm A* i zapisz wynik do zmiennej path
    astar(map, start_point, end_point)
    plt.show()
