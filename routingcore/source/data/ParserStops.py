import csv
from math import sin, cos, sqrt, atan2, radians

import json

inf = float('inf')

class ParserStops:

    def add_stop_to_stop_edges(graph, tag):
        data = {}

        with open("data/" + tag + "/stop_to_stop.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                stopid1 = line[0]
                stopid2 = line[1]
                cost = int(line[2])
                graph.add_edge(stopid1, stopid2, cost)
                graph.add_edge(stopid2, stopid1, cost)
        return data

    def add_stop_change_stop_edges(graph, tag):
        data = {}

        with open("data/" + tag + "/stop_change_stop.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                stopid1 = line[0]
                stopid2 = line[1]
                cost = int(line[2])
                graph.add_edge(stopid1, stopid2, cost)
                graph.add_edge(stopid2, stopid1, cost)
        return data


    def read_stops(tag, stopids):
        data = {}

        with open("data/" + tag + "/stops.txt", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                id = line[0]
                if id in stopids:
                    lat = float(line[3])
                    lng = float(line[4])
                    name = line[2]
                    data[id] = {
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    }
        return data

    def read_stops_TRAM(stopids):
        data = {}

        with open("data/TRAM/stops.txt", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                id = line[0]
                if id in stopids:
                    lat = float(line[3])
                    lng = float(line[4])
                    name = line[1]
                    data[id] = {
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    }
        return data

    def read_stops_FGC(stopids):
        data = {}

        with open("data/FGC/stops.txt", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                id = line[3]
                if id in stopids:
                    lat = float(line[0])
                    lng = float(line[1])
                    name = line[2]
                    data[id] = {
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    }
        return data

    def read_stoptimes(tag, stopids, stopsTMB):
        data = {}

        with open("data/" + tag + "/stop_times.txt", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                tripid = line[0]
                stopid = line[3]
                seq = line[4]

                if stopid in stopids:
                    if tripid in data:
                        tripstops = data[tripid]
                        tripstops[seq] = stopid
                        data[tripid] = tripstops
                    else:
                        data[tripid] = {str(seq): stopid}

        dataroutes = {}
        for tripid in data:
            keys = sorted(data[tripid].keys(), reverse=True)
            stops = []
            for key in keys:
                stops.append(data[tripid][key])
            dataroutes[tripid] = stops

        return dataroutes

    def read_trips(tag, stopids, stopsTMB, stoptimesTMB):
        data = {}

        with open("data/" + tag + "/trips.txt", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                routeid = line[0]
                tripid = line[2]

                #if routeid != "2" and routeid != "3":
                if not routeid in data and tripid in stoptimesTMB:
                    data[routeid] = stoptimesTMB[tripid]

        return data

    def read_routes(tag):
        data = {}

        with open("data/" + tag + "/routes.txt", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                routeid = line[0]
                name = line[1]
                
                data[routeid] = name

        return data

    def add_info_to_graph(graph, stopsTMB, tripsTMB, routesTMB):
        def find_route(stopid):
            for routeid in tripsTMB:
                if stopid in tripsTMB[routeid]:
                    return routeid
            return None

        data = {}

        llista_prohibida = ["Zona Universitària", "Avinguda de Xile", "Ernest Lluch", "Can Rigal", "Ca n'Oliveres", "Can Clota", 
            "Pont d'Esplugues", "La Sardana", "Montesa"]

        for routeid in tripsTMB:
            stopids = tripsTMB[routeid]

            for stopid in stopids:
                stopdata = stopsTMB[stopid]
                routeid = find_route(stopid)
                data[stopid] = {
                    "name": stopdata["name"],
                    "line": routesTMB[routeid],
                    "lat": stopdata["lat"],
                    "lng": stopdata["lng"]
                }

        graph.data.update(data)

    def get_path_info(graph, path):
        info = {"path": []}
        cost = 0
        lastline = None
        transbord = 0
        #for stopid in path:
        for i in range(0,len(path)):
            stopid = path[i]
            stopdata = graph.data[stopid]
            pathpoint = {
                "stopid": stopid,
                "stopname": stopdata["name"],
                "line": stopdata["line"],
                "lat": stopdata["lat"],
                "lng": stopdata["lng"],
                "cost": 0
            }

            key = None
            stopid1 = None
            stopid2 = None
            if i > 0:
                stopid1 = path[i-1]
                stopid2 = stopid
                key = stopid1 + "-" + stopid2

            shape = None
            if key is not None and key in graph.shape.keys():
                shape = graph.shape[key]
            elif lastline is not None and lastline == stopdata["line"]:
                print("ERROR --- " + str(key))

            if lastline is None:
                if key is None:
                    pathpoint["cost"] = 0
                else:
                    pathpoint["cost"] = graph.get_edge_cost(stopid1, stopid2)

                item = {}
                item["type"] = 'metro' if pathpoint["line"][0] == 'L' else 'tram'
                item["line"] = pathpoint["line"]
                item["path"] = [pathpoint]
                if key is None:
                    item["shape"] = []
                    item["cost"] = 0
                else:
                    item["shape"] = shape
                    item["cost"] = graph.get_edge_cost(stopid1, stopid2)
                item["transbord"] = 0
                info["path"].append(item)
                lastline = stopdata["line"]
            elif lastline != stopdata["line"]:
                if key is None:
                    pathpoint["cost"] = 0
                else:
                    pathpoint["cost"] = 0

                lastline = stopdata["line"]
                item = {}
                item["type"] = 'metro' if pathpoint["line"][0] == 'L' else 'tram'
                item["line"] = pathpoint["line"]
                item["path"] = [pathpoint]
                item["shape"] = []
                item["cost"] = 0
                info["path"].append(item)
                if key is not None:
                    item["transbord"] = graph.get_edge_cost(stopid1, stopid2)
                    transbord += graph.get_edge_cost(stopid1, stopid2)
                else:
                    item["transbord"] = 0
            else:
                if key is None:
                    pathpoint["cost"] = 0
                else:
                    pathpoint["cost"] = graph.get_edge_cost(stopid1, stopid2)

                info["path"][-1]["path"].append(pathpoint)
                if shape is not None:
                    info["path"][-1]["shape"].append(shape)
                    item["cost"] += graph.get_edge_cost(stopid1, stopid2)

        for i in range(0,len(path)-1):
            stopid1 = path[i]
            stopid2 = path[i+1]
            cost += graph.get_edge_cost(stopid1, stopid2)

        info["cost"] = cost
        info["transbord"] = transbord

        return info;

    def get_near_stopnodes(graph, lat, lng, maxdist=0.5):
        def distance_between_coords(lat1,lng1, lat2,lng2):
            # approximate radius of earth in km
            R = 6373.0

            lat1 = radians(lat1)
            lon1 = radians(lng1)
            lat2 = radians(lat2)
            lon2 = radians(lng2)
            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            return distance

        node1 = None
        node2 = None
        node3 = None
        dmax1 = inf
        dmax2 = inf
        dmax3 = inf
        for stopid in graph.data:
            # d is in kilometers
            d = distance_between_coords(lat, lng, graph.data[stopid]["lat"], graph.data[stopid]["lng"])
            
            if d <= maxdist:
                if d <= dmax1:
                    dmax1,dmax2,dmax3 = d,dmax1,dmax3
                    node1,node2,node3 = stopid,node1,node2
                elif d <= dmax2:
                    dmax2,dmax3 = d,dmax2
                    node2,node3 = stopid,node2
                elif d <= dmax3:
                    dmax3 = d
                    node3 = stopid

        return [node1, node2, node3]

    def get_path_shape(graph):
        def find_stopid(stopname, linename):
            for stopid in graph.data:
                stopdata = graph.data[stopid]
                name = stopdata["name"]
                line = stopdata["line"]

                if name == stopname and line == linename:
                    return stopid
            return None

        with open("data/E50m_XF_CAT_v1_LIN.geojson", "r", encoding='utf-8') as f:
            geojson = json.load(f)

        shape = {}

        for feature in geojson['features']:
            xarxa = feature['properties']['Xarxa']
            linia = feature['properties']['Linia']
            tram = feature['properties']['TRAM']
            serveis = feature['properties']['SERVEIS']
            tramsplit = tram.split("-")
            serveisplit = str(serveis).split("-")
            if tram != "Bifurcació" and "Cotxeres" not in tram and len(tramsplit) >= 2:
                fromcode = [0,1]
                tocode = [1,0]
                for i in range(0,len(fromcode)):
                    stopnamefrom = tramsplit[fromcode[i]]
                    stopnameto = tramsplit[tocode[i]]
                    stopidfrom = None
                    stopidto = None
                    for line in serveisplit:
                        if line != "None" and line not in ["L4", "L11", "L2", "T2", "T3", "T4", "T5", "T6", "L9L10", "L10"]:
                            stopidfrom = find_stopid(stopnamefrom, line)
                            stopidto = find_stopid(stopnameto, line)

                    if stopidfrom is not None and stopidto is not None:

                        coordinates = feature['geometry']["coordinates"][0]
                        coords = []
                        for c in coordinates:
                            lat = c[1]
                            lng = c[0]
                            coords.append({"lat": lat, "lng": lng})

                        shape[stopidfrom + "-" + stopidto] = coords


        graph.shape = shape




    
