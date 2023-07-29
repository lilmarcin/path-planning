from collections import deque
import matplotlib.pyplot as plt
import sys

    
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

def bfs(ax, map_obj, start_point, end_point, only_result):
    """
    Breadth-First Search (BFS) algorithm to find the shortest path between two points on the map.
    :param ax: plot on axes
    :param map_obj: Map class object (np. EmptyMap, QuadraticMap, LineMap)
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

    queue = deque([(start_point, [])])  # Queue with start_point and path to point
    plt.ion()
    visited = set()
    visited_points = set()

    print("Starting BFS...")
    while queue:
        current_point, path = queue.popleft()
        #print("Visited point:", current_point)
        visited_points.add(current_point)
        if only_result is False:
            draw_map(ax, map_obj, start_point, end_point, visited, path, current_point)
        if current_point == end_point:
            print("Path found", path + [current_point])
            draw_map(ax, map_obj, start_point, end_point, visited, path, current_point)
            return path + [current_point]

        visited.add(current_point)
        neighbors = [(current_point[0] + dx, current_point[1] + dy) for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]] # Up Down Left Right
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < x_range and 0 <= ny < y_range and (nx, ny) not in obstacles and (nx, ny) not in visited]

        for neighbor in valid_neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [current_point]))
    plt.ioff()
    plt.show()
    print("Path not found.")
    return None 