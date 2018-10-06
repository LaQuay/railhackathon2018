import csv

maxLatitude = 41.4
minLatitude = 41.1
maxLongitude = 2.1
minLongitude = 2.0

class ParserStops:

    def read_stops_TMB():
        data = {}

        with open("data/TMB/stops.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                lat = float(line[3])
                lng = float(line[4])
                if minLatitude <= lat <= maxLatitude and minLongitude <= lng <= maxLongitude:
                    id = line[0]
                    name = line[2]

                    data[id] = {
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    }
        return data

    def read_stoptimes_TMB(stopsTMB):
        data = {}
        #stopids = [d['id'] for d in stopsTMB]
        stopids = sorted(stopsTMB.keys(), reverse=True)

        with open("data/TMB/stop_times.txt", "r") as f:
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

    def read_trips_TMB(stopsTMB, stoptimesTMB):
        data = {}

        with open("data/TMB/trips.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                routeid = line[0]
                tripid = line[2]

                if not routeid in data and tripid in stoptimesTMB:
                    data[routeid] = stoptimesTMB[tripid]

        return data

    def add_routes_TMB(graph, stopsTMB, tripsTMB):
        data = {}

        for routeid in tripsTMB:
            stopids = tripsTMB[routeid]
            for i in range(0,len(stopids)-1):
                stopid1 = stopids[i]
                stopid2 = stopids[i+1]

                # TODO: cost of edge
                graph.add_edge(stopid1, stopid2, 5)

            for stopid in stopids:
                stopdata = stopsTMB[stopid]
                data[stopid] = {
                    "name": stopdata["name"],
                    "route": "ruta"
                }

        graph.data = data

    def get_path_info(graph, path):
        info = {"path": []}
        cost = 0
        for stopid in path:
            stopdata = graph.data[stopid]
            info["path"].append({
                "stopid": stopid,
                "stopname": stopdata["name"]
            })

            print(stopid + " --- " + stopdata["name"])

        for i in range(0,len(path)-1):
            stopid1 = path[i]
            stopid2 = path[i+1]
            cost += graph.get_edge_cost(stopid1, stopid2)

        info["cost"] = cost

        print(info)



    def read_stops_FGC():
        data = []

        with open("data/stops_FGC.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                lat = float(line[0])
                lng = float(line[1])
                if minLatitude <= lat <= maxLatitude and minLongitude <= lng <= maxLongitude:
                    id = line[3]
                    name = line[2]

                    data.append({
                        "id": id,
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    })
        return data