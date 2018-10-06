from flask import Flask
from flask_cors import CORS, cross_origin

import csv

from data.ParserStops import ParserStops

from Graph import Graph
from Algorithm import Algorithm
from flask import jsonify

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

inf = float('inf')

@app.route('/')
@cross_origin()
def index():
    return jsonify(get_dijkstra())

def get_dijkstra():
    path = algorithm.dijkstra("10", "1.317")
    info = ParserStops.get_path_info(algorithm.graph, path)
    print('Info gotten')
    print(str(info))
    return info

def init_graph():
    graph = Graph([])
    ParserStops.add_stop_to_stop_edges(graph, "TMB")
    ParserStops.add_stop_change_stop_edges(graph, "TMB")
    ParserStops.add_stop_to_stop_edges(graph, "TRAM")
    ParserStops.add_stop_change_stop_edges(graph, "TRAM")
    #ParserStops.add_stop_to_stop_edges(graph, "FGC")
    #ParserStops.add_stop_change_stop_edges(graph, "FGC")
    #graph.print_graph()

    stopids = graph.vertices
    #print(stopids)

    # TMB data
    stopsTMB = ParserStops.read_stops("TMB", stopids)
    stoptimesTMB = ParserStops.read_stoptimes("TMB", stopids, stopsTMB)
    tripsTMB = ParserStops.read_trips("TMB", stopids, stopsTMB, stoptimesTMB)
    routesTMB = ParserStops.read_routes("TMB")

    # TRAM data
    stopsTRAM = ParserStops.read_stops_TRAM(stopids)
    stoptimesTRAM = ParserStops.read_stoptimes("TRAM", stopids, stopsTRAM)
    tripsTRAM = ParserStops.read_trips("TRAM", stopids, stopsTRAM, stoptimesTRAM)
    routesTRAM = ParserStops.read_routes("TRAM")

    # FGC data
    #stopsFGC = ParserStops.read_stops_FGC(stopids)
    #stoptimesFGC = ParserStops.read_stoptimes("FGC", stopids, stopsFGC)
    #tripsFGC = ParserStops.read_trips("FGC", stopids, stopsFGC, stoptimesFGC)
    #routesFGC = ParserStops.read_routes("FGC")

    ParserStops.add_info_to_graph(graph, stopsTMB, tripsTMB, routesTMB)
    ParserStops.add_info_to_graph(graph, stopsTRAM, tripsTRAM, routesTRAM)
   #ParserStops.add_info_to_graph(graph, stopsFGC, tripsFGC, routesFGC)

    return Algorithm(graph)


algorithm = init_graph()
path = get_dijkstra()

algorithm.graph.update_edge("1.516","1.517",inf)
path = get_dijkstra()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
