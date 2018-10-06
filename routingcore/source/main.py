from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from data.ParserStops import ParserStops
from Graph import Graph
from Algorithm import Algorithm

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

inf = float('inf')


@app.route('/get-dijkstra/<float:latitude>/<float:longitude>/<float:latitude2>/<float:longitude2>/', methods=['GET'])
@cross_origin()
def index(latitude, longitude, latitude2, longitude2):
    return jsonify(get_dijkstra(
        coordfrom={"lat": latitude, "lng": longitude},
        coordto={"lat": latitude2, "lng": longitude2}))



@app.route('/update-edge/<string:node1>/<string:node2>/<int:newcost>/', methods=['POST'])
@cross_origin()
def index2(node1, node2, newcost):
    algorithm.graph.update_edge(node1, node2, newcost)
    return ""


def get_dijkstra(coordfrom, coordto):
    maxdist = 0.5
    nodefroms = ParserStops.get_near_stopnodes(algorithm.graph, coordfrom["lat"], coordfrom["lng"], maxdist)
    nodetos = ParserStops.get_near_stopnodes(algorithm.graph, coordto["lat"], coordto["lng"], maxdist)

    mininfo = None
    mincost = inf
    for nodefrom in nodefroms:
        for nodeto in nodetos:
            if nodefrom is not None and nodeto is not None:
                path = algorithm.dijkstra(nodefrom, nodeto)
                info = ParserStops.get_path_info(algorithm.graph, path)

                cost = info["cost"]
                if cost < mincost:
                    mincost = cost
                    mininfo = info

    #print(mininfo)

    return mininfo


def init_graph():
    graph = Graph([])
    ParserStops.add_stop_to_stop_edges(graph, "TMB")
    ParserStops.add_stop_change_stop_edges(graph, "TMB")
    ParserStops.add_stop_to_stop_edges(graph, "TRAM")
    ParserStops.add_stop_change_stop_edges(graph, "TRAM")
    # ParserStops.add_stop_to_stop_edges(graph, "FGC")
    # ParserStops.add_stop_change_stop_edges(graph, "FGC")
    # graph.print_graph()

    stopids = graph.vertices
    # print(stopids)

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
    # stopsFGC = ParserStops.read_stops_FGC(stopids)
    # stoptimesFGC = ParserStops.read_stoptimes("FGC", stopids, stopsFGC)
    # tripsFGC = ParserStops.read_trips("FGC", stopids, stopsFGC, stoptimesFGC)
    # routesFGC = ParserStops.read_routes("FGC")

    ParserStops.add_info_to_graph(graph, stopsTMB, tripsTMB, routesTMB)
    ParserStops.add_info_to_graph(graph, stopsTRAM, tripsTRAM, routesTRAM)
    # ParserStops.add_info_to_graph(graph, stopsFGC, tripsFGC, routesFGC)

    ParserStops.get_path_shape(graph)

    return Algorithm(graph)


algorithm = init_graph()

info = get_dijkstra(coordfrom={"lat": 41.3926816, "lng": 2.1444228}, coordto={"lat": 41.3755693, "lng": 2.1284559})
algorithm.graph.update_edge("1.317", "1.318", 100)
info = get_dijkstra(coordfrom={"lat": 41.3926816, "lng": 2.1444228}, coordto={"lat": 41.3755693, "lng": 2.1284559})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
