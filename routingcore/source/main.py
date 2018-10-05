from flask import Flask
from flask_cors import CORS, cross_origin

import csv

from data.ParserStops import ParserStops

from Graph import Graph
from Algorithm import Algorithm

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return "jeje"
    return "Dijkstra A to E: " + str(get_dijkstra())


def get_dijkstra():
    return algorithm.dijkstra("a", "e")




def init_graph():
    stopsTMB = ParserStops.read_stops_TMB()
    stoptimesTMB = ParserStops.read_stoptimes_TMB(stopsTMB)
    tripsTMB = ParserStops.read_trips_TMB(stopsTMB, stoptimesTMB)

    stopsFGC = ParserStops.read_stops_FGC()

    graph = Graph([])
    #ParserStops.add_routes_TMB(graph, stopsTMB, stoptimesTMB)
    
    graph.print_graph()
    #print(str(stopsTMB))
    #print(str(stopsFGC))

    return Algorithm(graph)


algorithm = init_graph()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
