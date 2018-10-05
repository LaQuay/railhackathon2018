import csv

maxLatitude = 41.4
minLatitude = 41.1
maxLongitude = 2.1
minLongitude = 2.0

class ParserStops:

    def read_stops_TMB():
        data = []

        with open("data/TMB/stops.txt", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)
            for i, line in enumerate(reader):
                lat = float(line[3])
                lng = float(line[4])
                if minLatitude <= lat <= maxLatitude and minLongitude <= lng <= maxLongitude:
                    id = line[0]
                    name = line[2]

                    data.append({
                        "id": id,
                        "name": name,
                        "lat": lat,
                        "lng": lng
                    })
        return data

    def read_stoptimes_TMB(stopsTMB):
        data = {}
        stopids = [d['id'] for d in stopsTMB]

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
                    #data[routeid] = tripid
                    data[routeid] = stoptimesTMB[tripid]

        return data


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