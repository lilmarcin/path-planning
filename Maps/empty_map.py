"""
Plot 2D map 20x20

                                                                                
***********************************
*                                 * 
*                                 *
*                                 *
*                                 * 
*                                 * 
*                                 *
*                                 *
*                                 * 
*                                 *
*                                 *
***********************************
"""
import matplotlib.pyplot as plt

class EmptyMap:
    def __init__(self):
        self.x_range = 10 # x size of grid
        self.y_range = 10 # y size of grid
        self.obstacles = self.obstacles_map()
        self.obstacles_lines = self.obstacles_lines_map()

    def obstacles_map(self):
        x = self.x_range+1
        y = self.y_range+1
        obstacles = set()

        # Outer Walls
        for i in range(x):
            obstacles.add((i, 0))
        for i in range(x):
            obstacles.add((i, y - 1))

        for i in range(y):
            obstacles.add((0, i))
        for i in range(y):
            obstacles.add((x - 1, i))
        return obstacles
    
    def obstacles_lines_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = self.x_range
        y = self.y_range
        obstacles_lines = set()

        # Outer Walls
        obstacles_lines = [
            [(0, 0), (x, 0)],      # Bottom Wall 
            [(x, 0), (x, y)],    # Right Wall
            [(x, y), (0, y)],    # Top Wall
            [(0, y), (0, 0)]      # Left Wall
        ]

        return obstacles_lines

""" if __name__ == "__main__":
    map = EmptyMap()

    # Rysuj ściany
    for obstacle in map.obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        plt.plot(x_coords, y_coords, color='black', linewidth=5)

    plt.xlim(0, map.x_range)
    plt.ylim(0, map.y_range)
    plt.grid(True)
    plt.show()
 """