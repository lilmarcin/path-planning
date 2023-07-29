"""
Create 2D maze 10x10
uncomment main to see shape
"""
import matplotlib.pyplot as plt

class Maze2:
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

        for i in range(0, 6):
            obstacles.add((i, 8))

        obstacles.add((1, 7))
        obstacles.add((1, 5))
        obstacles.add((1, 4))

        for i in range(0, 6):
            obstacles.add((i, 2))

        for i in range(2, 4):
            obstacles.add((5, i))

        for i in range(5, 8):
            obstacles.add((i, 4))

        obstacles.add((7, 2))
        for i in range(7, 10):
            obstacles.add((i, 1))

        for i in range(1, 5):
            obstacles.add((9, i))

        for i in range(4, 7):
            obstacles.add((3, i))

        for i in range(3, 10):
            obstacles.add((i, 6)) 

        obstacles.add((9, 7))    
        obstacles.add((7, 8))    
        obstacles.add((7, 9)) 
        obstacles.add((8, 9))    

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
            [(0, 8), (5, 8)],
            [(0, 7), (1, 7)],
            [(0, 5), (1, 5)],
            [(1, 7), (1, 8)],
            [(1, 4), (1, 5)],
            [(0, 4), (1, 4)],
            [(0, 2), (5, 2)],
            [(5, 2), (5, 4)],      
            [(5, 4), (7, 4)], 
            [(7, 2), (7, 0)], 
            [(7, 1), (9, 1)], 
            [(9, 1), (9, 4)], 
            [(3, 4), (3, 6)], 
            [(3, 6), (9, 6)], 
            [(9, 6), (9, 7)], 
            [(9, 7), (10, 7)],
            [(7, 8), (7, 10)],
            [(7, 9), (8, 9)],
        ]

        return obstacles_lines
    
""" if __name__ == "__main__":

    map = Maze2()

    # Plot obstacles
    for obstacle in map.obstacles_lines:
        x_coords, y_coords = zip(*obstacle)
        plt.plot(x_coords, y_coords, color='black', linewidth=1)     

    for obstacle in map.obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='red', s=50)   
    plt.xlim(0, map.x_range)
    plt.ylim(0, map.y_range)
    plt.grid(True)
    plt.show() """

