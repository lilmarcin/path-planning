import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.gridspec import GridSpec
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

start_point = (1, 1)
end_point = (5, 9)

def show_message(message):
    ax.text(0.5, 1.05, message, fontsize=14, ha='center', va='center', transform=ax.transAxes)
    plt.draw()
    #plt.pause(1)

def on_start_x_change(text):
    global start_point
    try:
        x = int(text)
        start_point = (x, start_point[1]) if start_point else None
    except ValueError:
        print("Invalid input for start point x. Use integer value.")

def on_start_y_change(text):
    global start_point
    try:
        y = int(text)
        start_point = (start_point[0], y) if start_point else None
    except ValueError:
        print("Invalid input for start point y. Use integer value.")

def on_end_x_change(text):
    global end_point
    try:
        x = int(text)
        end_point = (x, end_point[1]) if end_point else None
    except ValueError:
        print("Invalid input for end point x. Use integer value.")

def on_end_y_change(text):
    global end_point
    try:
        y = int(text)
        end_point = (end_point[0], y) if end_point else None
    except ValueError:
        print("Invalid input for end point y. Use integer value.")

def on_set_clicked(event, map_obj):
    global start_point, end_point
    print("Start point set:", start_point)
    print("End point set:", end_point)
    if intersect_obstacle(map_obj, start_point, end_point):
        ax.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
        ax.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')
        clear_plot(ax)
        show_message("Start point and end point must not be in the obstacle!")
    else:
        ax.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
        ax.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')
        clear_plot(ax)

def clear_plot(ax):
    ax.clear()
    for obstacle in map.obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        ax.plot(x_coords, y_coords, color='black', linewidth=1)
    ax.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
    ax.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')
    ax.grid(True)
    ax.set_xlim(0, map.x_range)
    ax.set_ylim(0, map.y_range)
    plt.draw()


def on_start_planning_clicked(event):
    global start_point, end_point
    astar(map, start_point, end_point)

def draw_map(map_obj, visited_points, path, current_point=None):
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
        ax.scatter(point[0], point[1], color='gray', s=5)

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
        ax.scatter(end_point[0], end_point[1], color='green', s=100, label='End Point')
        ax.plot([path[-1][0], end_point[0]], [path[-1][1], end_point[1]], color='red')
        
    ax.set_xlim(0, x_range)
    ax.set_ylim(0, y_range)
    ax.grid(True)
    plt.pause(0.001)

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

def astar(map_obj, start_point, end_point):
    """
    A* algorithm to find the shortest path between two points on the map.

    :param map_obj: Map class object (np. EmptyMap, QuadraticMap, LineMap)
    :param start_point: Coordinates of the start point in the format (x, y)
    :param end_point: Coordinates of the end point in the format (x, y)
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
        draw_map(map_obj, visited, path, current_point) # Uncomment to draw every node added to the tree
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
    map = QuadraticMap()
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(1, 2, width_ratios=[3, 1])
    ax = plt.subplot(gs[0])
    ax.set_xlim(0, map.x_range)
    ax.set_ylim(0, map.y_range)

    for obstacle in map.obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        ax.plot(x_coords, y_coords, color='black', linewidth=1)

    ax.grid(True)
    ax_right = plt.subplot(gs[1])
    ax_right.axis('off')
    ax_start_x_textbox = plt.axes([0.75, 0.8, 0.03, 0.05], facecolor='lightblue')
    ax_start_y_textbox = plt.axes([0.8, 0.8, 0.03, 0.05], facecolor='lightblue')
    ax_end_x_textbox = plt.axes([0.75, 0.7, 0.03, 0.05], facecolor='paleturquoise')
    ax_end_y_textbox = plt.axes([0.8, 0.7, 0.03, 0.05], facecolor='paleturquoise')

    text_box_start_x = TextBox(ax_start_x_textbox, 'Start point    x:', initial=str(start_point[0]))
    text_box_start_y = TextBox(ax_start_y_textbox, 'y:', initial=str(start_point[1]))
    text_box_end_x = TextBox(ax_end_x_textbox, 'End point    x:', initial=str(end_point[0]))
    text_box_end_y = TextBox(ax_end_y_textbox, 'y:', initial=str(end_point[1]))

    text_box_start_x.on_submit(on_start_x_change)
    text_box_start_y.on_submit(on_start_y_change)
    text_box_end_x.on_submit(on_end_x_change)
    text_box_end_y.on_submit(on_end_y_change)

    ax_set_button = plt.axes([0.75, 0.6, 0.05, 0.05], facecolor='gray')
    set_button = Button(ax_set_button, 'Set', color='white', hovercolor='lightgray')
    set_button.on_clicked(lambda event: on_set_clicked(event, map))

    ax_start_planning_button = plt.axes([0.75, 0.5, 0.1, 0.05], facecolor='green')
    start_planning_button = Button(ax_start_planning_button, 'Start Planning', color='white', hovercolor='lightgray')
    start_planning_button.on_clicked(on_start_planning_clicked)
    #astar(map, start_point, end_point)
    plt.show()
