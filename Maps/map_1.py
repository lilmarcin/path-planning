"""
Plot 2D map

"""
import matplotlib.pyplot as plt

class QuadraticMap:
    def __init__(self):
        self.x_range = 10 # x size of grid
        self.y_range = 10 # y size of grid
        self.obstacles = self.obstacles_map()

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

        # 4 squares inside
        square_size = 2
        for i in range(square_size):
            for j in range(square_size):
                obstacles.add((4 - square_size // 2 + i, 4 - square_size // 2 + j))

        for i in range(square_size):
            for j in range(square_size):
                obstacles.add((7 - square_size // 2 + i, 4 - square_size // 2 + j))

        for i in range(square_size):
            for j in range(square_size):
                obstacles.add((4 - square_size // 2 + i, 8 - square_size // 2 + j))

        for i in range(square_size):
            for j in range(square_size):
                obstacles.add((7 - square_size // 2 + i, 8 - square_size // 2 + j))

        return obstacles
    
""" if __name__ == "__main__":

    map = QuadraticMap()
    x_range = map.x_range
    y_range = map.y_range
    obstacles = map.obstacles

    # Plot obstacles
    for obstacle in obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='black', s=100)
        
    plt.xlim(0, x_range)
    plt.ylim(0, y_range)
    plt.grid(True)
    plt.show()
 """