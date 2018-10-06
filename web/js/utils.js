(() => {
  window.Koalas = {}
  var Koalas = window.Koalas

  Koalas.DataAccess = {}

  var API_URL = "/api";

  Koalas.Resources = {
    useMocks: false,
    apiUrl: API_URL
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