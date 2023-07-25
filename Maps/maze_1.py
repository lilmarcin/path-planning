"""
Create 2D maze 10x10
uncomment main to see shape
"""
import matplotlib.pyplot as plt

class Maze1:
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

        obstacles.add((1, 5))

        for i in range(2, 9):
            obstacles.add((3, i))

        for i in range(2, 6):
            obstacles.add((7, i))

        for i in range(7, 10):
            obstacles.add((7, i))

        for i in range(3, 9):
            obstacles.add((i, 3))

        for i in range(3, 9):
            obstacles.add((i, 7))
        return obstacles
    
    def obstacles_lines_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        """

        x = self.x_range
        y = self.y_range
        obstacles_lines = set()

        # Outer walls
        obstacles_lines = [
            [(0, 0), (10, 0)],      # Bottom Wall 
            [(10, 0), (10, 10)],    # Right Wall
            [(10, 10), (0, 10)],    # Top Wall
            [(0, 10), (0, 0)],      # Left Wall

        # Create walls inside
            [(0, 5), (1, 5)],
            [(3, 2), (3, 8)],
            [(7, 2), (7, 5)],
            [(7, 7), (7, 10)],
            [(3, 3), (8, 3)],
            [(3, 7), (8, 7)],
        ]

        return obstacles_lines
    
if __name__ == "__main__":

    map = Maze1()

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

