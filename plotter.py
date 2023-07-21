"""
Plot 2D grid
"""
import matplotlib.pyplot as plt
from maps.map_1 import QuadraticMap
from maps.map_2 import LineMap
from maps.map_3 import EmptyMap
from path_planning.BFS.bfs import bfs

def draw_map(map_obj, start_point, end_point, bfs_path=None):
    """
    Draw map with start and end points.
    
    :param map_obj: Map class object (np. QuadraticMap, AnotherMap, YetAnotherMap)
    :param start_point: Coordinates of the start point in the format (x, y)
    :param end_point: Coordinates of the end point in the format (x, y)
    """

    # Pobierz przeszkody z obiektu mapy
    obstacles = map_obj.obstacles

    # Wyciągnij zakresy mapy z obiektu mapy
    x_range = map_obj.x_range
    y_range = map_obj.y_range

    # Narysuj mapę
    plt.figure(figsize=(8, 8))
    plt.xlim(0, x_range)
    plt.ylim(0, y_range)

    for obstacle in obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='red', s=30)

    # Draw start and end point using scatter plot
    plt.scatter(start_point[0], start_point[1], color='green', s=50, label='Start')
    plt.scatter(end_point[0], end_point[1], color='red', s=50, label='End')

    if bfs_path:
            # Draw BFS path
            x_coords = [point[0] for point in bfs_path]
            y_coords = [point[1] for point in bfs_path]
            plt.plot(x_coords, y_coords, color='blue', linewidth=2)

    plt.legend(loc="lower left", bbox_to_anchor=(0, 1.02, 1, 0.2))
    plt.grid()
    plt.show()

if __name__ == "__main__":

    """
    Available map:
    -QuadraticMap()
    -LineMap()
    -EmptyMap()
    """    
    map = EmptyMap()
    start_point = (5, 5)
    end_point = (15, 15)
    bfs_path = bfs(map, start_point, end_point)
    draw_map(map, start_point, end_point, bfs_path)