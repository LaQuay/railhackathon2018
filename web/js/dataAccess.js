(() => {
  Koalas.DataAccess.Routing = () => {
    var _this = {}

    _this.getRoute = (origin, destination) => {
      var promise = new Promise((resolve, reject) => {
        var url = `${Koalas.Resources.apiUrl}/get-dijkstra/${origin[0]}/${origin[1]}/${destination[0]}/${destination[1]}/`;
        $.get(url)
          .then(response => {
            resolve(response)
          })
      })
      return promise
    };

    return _this
  }

  Koalas.DataAccess.Metro = () => {
    var _this = {}

    _this.getMetroStations = () => {
      var promise = new Promise((resolve, reject) => {
        resolve(metroStationsMock)
      })
      return promise
    }

    return _this
  }
})();