"""
Plot 2D map
"""

import matplotlib.pyplot as plt

class LineMap:
    def __init__(self):
        self.x_range = 10 # x size of grid
        self.y_range = 10 # y size of grid
        self.obstacles = self.obstacles_map()
        self.obstacles_lines = self.obstacles_lines_map()

    def update_obstacles(self, obstacles):
        self.obs = obstacles

    def obstacles_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

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

        for i in range(3, 10):
            obstacles.add((i, 7))

        for i in range(0, 8):
            obstacles.add((i, 3))

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
            [(0, 0), (10, 0)],      # Bottom Wall 
            [(10, 0), (10, 10)],    # Right Wall
            [(10, 10), (0, 10)],    # Top Wall
            [(0, 10), (0, 0)],      # Left Wall

            [(3, 7), (10, 7)],      # Bottom Left Wall 
            [(0, 3), (7, 3)],       # Top Right Wall
        ]

        return obstacles_lines  
    
if __name__ == "__main__":

    map = LineMap()

    # Plot obstacles
    for obstacle in map.obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        plt.plot(x_coords, y_coords, color='black', linewidth=1)     

    for obstacle in map.obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='red', s=50)   
    plt.xlim(0, map.x_range)
    plt.ylim(0, map.y_range)
    plt.grid(True)
    plt.show()
