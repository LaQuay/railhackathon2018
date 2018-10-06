(() => {
  window.Koalas = {}
  var Koalas = window.Koalas

  Koalas.Resources = {
    useMocks: true
  }

  Koalas.Util = {}

  Koalas.Util.getDataAccess = (className) => {
    var instance = null
    if (Koalas.Resources.useMocks) {
      instance = Koalas.DataAccess[className + 'Mock']()
      console.log(instance)
    } else {
      instance = Koalas.DataAccess[className]()
    }
    return instance
  }
})();