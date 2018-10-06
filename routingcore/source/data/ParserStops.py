import csv

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

        with open("data/" + tag + "/stops.txt", "r") as f:
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

        with open("data/TRAM/stops.txt", "r") as f:
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

        with open("data/FGC/stops.txt", "r") as f:
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

        with open("data/" + tag + "/stop_times.txt", "r") as f:
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

        with open("data/" + tag + "/trips.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                routeid = line[0]
                tripid = line[2]

                if not routeid in data and tripid in stoptimesTMB:
                    data[routeid] = stoptimesTMB[tripid]

        return data

    def read_routes(tag):
        data = {}

        with open("data/" + tag + "/routes.txt", "r") as f:
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

        for routeid in tripsTMB:
            stopids = tripsTMB[routeid]

            for stopid in stopids:
                stopdata = stopsTMB[stopid]
                routeid = find_route(stopid)
                data[stopid] = {
                    "name": stopdata["name"],
                    "line": routesTMB[routeid]
                }

        graph.data.update(data)

    def get_path_info(graph, path):
        print("PATH ----------------")

        info = {"path": []}
        cost = 0
        for stopid in path:
            stopdata = graph.data[stopid]
            info["path"].append({
                "stopid": stopid,
                "stopname": stopdata["name"],
                "line": stopdata["line"]
            })

            print(stopid + " --- " + stopdata["name"] + " --- " + stopdata["line"])

        for i in range(0,len(path)-1):
            stopid1 = path[i]
            stopid2 = path[i+1]
            cost += graph.get_edge_cost(stopid1, stopid2)

        info["cost"] = cost
