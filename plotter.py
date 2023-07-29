"""
Plot 2D grid
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, CheckButtons, RadioButtons
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

from Maps.empty_map import EmptyMap
from Maps.map_1 import QuadraticMap
from Maps.map_2 import LineMap
from Maps.maze_1 import Maze1
from Maps.maze_2 import Maze2

from PathPlanning.AStar.astar import astar, intersect_obstacle
from PathPlanning.Dijkstra.dijkstra import dijkstra
from PathPlanning.RapidlyExploringRandomTree.rrt import rrt
from PathPlanning.RapidlyExploringRandomTree.rrt_star import rrt_star
from PathPlanning.RapidlyExploringRandomTree.rrt_connect import rrt_connect
from PathPlanning.BreadthFirstSearch.bfs import bfs
from PathPlanning.DepthFirstSearch.dfs import dfs

start_point = (1, 1)
end_point = (9, 9)
map = EmptyMap()
algorithm = 'A*'
only_result = True

def show_message(message):
    ax_left.text(0.5, 1.05, message, fontsize=14, ha='center', va='center', transform=ax_left.transAxes)
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

def on_set_clicked(event, map_obj):
    global start_point, end_point
    print("Start point set:", start_point)
    print("End point set:", end_point)
    if intersect_obstacle(map_obj, start_point, end_point):
        ax_left.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
        ax_left.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')
        clear_plot(ax_left)
        show_message("Start point and end point must not be in the obstacle!")
    else:
        ax_left.scatter(start_point[0], start_point[1], color='blue', s=100, label='Start Point')
        ax_left.scatter(end_point[0], end_point[1], color='teal', s=100, label='End Point')
        clear_plot(ax_left)

def on_map_button_click(event, map_name):
    global map
    map = map_name
    clear_plot(ax_left)
    for obstacle in map.obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        ax_left.plot(x_coords, y_coords, color='black', linewidth=1)

def on_checkbox_clicked(label):
    global only_result
    if label == 'Show Only Result':
        only_result = not only_result

def on_algorithm_button_click(label):
    global algorithm
    algorithm = label

def on_start_planning_clicked(event):
    global start_point, end_point, algorithm

    if algorithm == 'A*':
        astar(ax_left, map, start_point, end_point, only_result)
    elif algorithm == 'Dijkstra':
        dijkstra(ax_left, map, start_point, end_point, only_result)
    elif algorithm == 'RRT':
        rrt(ax_left, map, start_point, end_point, only_result, max_points=10000)
    elif algorithm == 'RRT*':
        rrt_star(ax_left, map, start_point, end_point, only_result, max_points=10000, rewire_radius=0.5)
    elif algorithm == 'RRT-Connect':
        rrt_connect(ax_left, map, start_point, end_point, only_result, max_points=10000)
    elif algorithm == 'BFS':
        bfs(ax_left, map, start_point, end_point, only_result)
    elif algorithm == 'DFS':
        dfs(ax_left, map, start_point, end_point, only_result)
    else:
        show_message("Please select an algorithm.")


if __name__ == "__main__":
    
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(1, 3, width_ratios=[3, 1, 1])
    ax_left = plt.subplot(gs[0])
    ax_left.set_xlim(0, map.x_range)
    ax_left.set_ylim(0, map.y_range)


    ax_left.grid(True)
    ax_center = plt.subplot(gs[1])
    ax_center.axis('off')


    EmptyMap_button = Button(plt.axes([0.55, 0.8, 0.09, 0.03]), 'EmptyMap', color='white', hovercolor='lightblue')
    LineMap_button = Button(plt.axes([0.55, 0.75, 0.09, 0.03]), 'LineMap', color='white', hovercolor='lightblue')
    QuadraticMap_button = Button(plt.axes([0.55, 0.7, 0.09, 0.03]), 'QuadraticMap', color='white', hovercolor='lightblue')
    Maze1_button = Button(plt.axes([0.55, 0.65, 0.09, 0.03]), 'Maze1', color='white', hovercolor='lightblue')
    Maze2_button = Button(plt.axes([0.55, 0.6, 0.09, 0.03]), 'Maze2', color='white', hovercolor='lightblue')

    EmptyMap_button.on_clicked(lambda event: on_map_button_click(event, EmptyMap()))
    LineMap_button.on_clicked(lambda event: on_map_button_click(event, LineMap()))
    QuadraticMap_button.on_clicked(lambda event: on_map_button_click(event, QuadraticMap()))
    Maze1_button.on_clicked(lambda event: on_map_button_click(event, Maze1()))
    Maze2_button.on_clicked(lambda event: on_map_button_click(event, Maze2()))

    algorithm_button = RadioButtons(plt.axes([0.7, 0.5, 0.15, 0.35]), ('A*', 'Dijkstra', 'RRT', 'RRT*','RRT-Connect','BFS', 'DFS' ))
    algorithm_button.on_clicked(on_algorithm_button_click)

    ax_start_x_textbox = plt.axes([0.64, 0.4, 0.03, 0.05])
    ax_start_y_textbox = plt.axes([0.7, 0.4, 0.03, 0.05])
    ax_end_x_textbox = plt.axes([0.64, 0.3, 0.03, 0.05])
    ax_end_y_textbox = plt.axes([0.7, 0.3, 0.03, 0.05])

    text_box_start_x = TextBox(ax_start_x_textbox, 'Start point   x:', initial=str(start_point[0]))
    text_box_start_y = TextBox(ax_start_y_textbox, 'y:', initial=str(start_point[1]))
    text_box_end_x = TextBox(ax_end_x_textbox, 'End point   x:', initial=str(end_point[0]))
    text_box_end_y = TextBox(ax_end_y_textbox, 'y:', initial=str(end_point[1]))

    text_box_start_x.on_submit(on_start_x_change)
    text_box_start_y.on_submit(on_start_y_change)
    text_box_end_x.on_submit(on_end_x_change)
    text_box_end_y.on_submit(on_end_y_change)

    ax_set_button = plt.axes([0.65, 0.225, 0.05, 0.05])
    set_button = Button(ax_set_button, 'Set', color='teal', hovercolor='paleturquoise')
    set_button.on_clicked(lambda event: on_set_clicked(event, map))

    ax_start_planning_button = plt.axes([0.625, 0.17, 0.1, 0.05])
    start_planning_button = Button(ax_start_planning_button, 'Start Planning', color='green', hovercolor='lightgreen')
    start_planning_button.on_clicked(on_start_planning_clicked)

    check = CheckButtons(plt.axes([0.6, 0.115, 0.15, 0.05]), ['Show Only Result'], [True])
    check.on_clicked(on_checkbox_clicked)
    plt.show()
