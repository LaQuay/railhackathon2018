from flask import Flask
from flask_cors import CORS, cross_origin

from Graph import Graph
from Algorithm import Algorithm

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return "Dijkstra A to E: " + str(get_dijkstra())


def get_dijkstra():
    return algorithm.dijkstra("a", "e")


def init_graph():
    graph = Graph([
        ("a", "b", 7), ("b", "a", 7), ("a", "c", 9), ("a", "f", 14), ("b", "c", 10),
        ("b", "d", 15), ("c", "d", 11), ("c", "f", 2), ("d", "e", 6),
        ("e", "f", 9)])

    return Algorithm(graph)


algorithm = init_graph()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
