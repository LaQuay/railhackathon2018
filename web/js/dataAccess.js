(() => {
  Koalas.DataAccess.Routing = () => {
    var _this = {}

    _this.getRoute = (origin, destination) => {
      var promise = new Promise((resolve, reject) => {
        $.get(`${Koalas.Resources.apiUrl}/`)
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