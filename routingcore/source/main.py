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
    return "Dijkstra A to E: " + str(get_dijkstra())

def get_dijkstra():
    path = algorithm.dijkstra("1.516", "1.315")
    ParserStops.get_path_info(algorithm.graph, path)

    return path

def init_graph():
    graph = Graph([])
    ParserStops.add_stop_to_stop_edges_TMB(graph)
    ParserStops.add_stop_change_stop_edges_TMB(graph)
    #graph.print_graph()

    stopids = graph.vertices
    #print(stopids)

    # TMB data
    stopsTMB = ParserStops.read_stops_TMB(stopids)
    stoptimesTMB = ParserStops.read_stoptimes_TMB(stopids, stopsTMB)
    tripsTMB = ParserStops.read_trips_TMB(stopids, stopsTMB, stoptimesTMB)
    routesTMB = ParserStops.read_routes_TMB()
    
    ParserStops.add_info_TMB(graph, stopsTMB, tripsTMB, routesTMB)

    # FGC data
    #stopsFGC = ParserStops.read_stops_FGC()

    
    #print(str(stopsTMB))
    #print(str(stopsFGC))

    return Algorithm(graph)


algorithm = init_graph()
print(str(get_dijkstra()))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
