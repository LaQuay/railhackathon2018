(() => {
  Koalas.DataAccess = {}

  Koalas.DataAccess.RoutingMock = () => {
    var _this = {}

    _this.getRoute = (origin, desination) => {
      var promise = new Promise((resolve, reject) => {
        resolve(routeMock)
      })
      return promise
    };

    return _this
  }

  Koalas.DataAccess.MetroMock = () => {
    var _this = {}

    _this.getMetroStations = () => {
      var promise = new Promise((resolve, reject) => {
        resolve(metroStationsMock)
      })
      return promise
    }

    return _this
  }

  // MOCKS
  var routeMock = [
    {
      type: 'walk',
      path: [
        [41.376193, 2.121745],
        [41.375697, 2.121762],
        [41.375794, 2.118059]
      ]
    },
    {
      type: 'metro',
      line: 'L5',
      color: '#37f',
      path: [
        [41.375794, 2.118059],
        [41.373803, 2.107211],
        [41.371668, 2.099704]
      ]
    },
    {
      type: 'walk',
      path: [
        [41.371668, 2.099704],
        [41.371374, 2.099516]
      ]
    }
  ]

  var metroStationsMock = [
    [
      {
        id: 12313415,
        name: 'Collblanc',
        location: [41.376193, 2.121745]
      },
      {
        id: 1231451,
        name: 'Pubilla Cases',
        location: [41.373785, 2.107301]
      },
      {
        id: 235512,
        name: 'Can Vidalet',
        location: [41.371374, 2.099516]
      }
    ]
  ]
})();