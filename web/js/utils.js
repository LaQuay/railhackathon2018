(() => {
  window.Koalas = {}
  var Koalas = window.Koalas

  Koalas.DataAccess = {}

  Koalas.Resources = {
    useMocks: false,
    apiUrl: 'http://localhost:5000'
  }

  Koalas.Util = {}

  Koalas.Util.getDataAccess = (className) => {
    var instance = null
    if (Koalas.Resources.useMocks) {
      instance = Koalas.DataAccess[className + 'Mock']()
    } else {
      instance = Koalas.DataAccess[className]()
    }
    return instance
  }
})();