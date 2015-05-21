var services = angular.module('ngdocket.services', ['ngResource']);

services.factory('SearchFactory', function ($resource) {
    return $resource('http://pucscrape.appspot.com/', {}, {
        show: { method: 'GET', params: {api_id: 'd4dc4045dd431d43b317190a41b982aa'}  }
    })
});