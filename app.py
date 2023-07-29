from flask import Flask, render_template, request
import random 
from Maps.empty_map import EmptyMap
from Maps.map_1 import QuadraticMap
from Maps.map_2 import LineMap
from Maps.maze_1 import Maze1

app = Flask(__name__)

# Tu umieść swoje funkcje RRT* i funkcje do rysowania mapy
# np. rrt_star, draw_map, euclidean_distance, itp.


maps = {
    'empty_map': EmptyMap(),
    'map_1': QuadraticMap(),
    'map_2': LineMap(),
    'map_3': Maze1(),
    # Dodaj tutaj kolejne mapy
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_map = request.form.get('map')
        if selected_map:
            map_data = maps[selected_map]
            return render_template('index.html', map_data=map_data)

    return render_template('index.html', maps=maps.keys())

if __name__ == '__main__':
    app.run(debug=True)
