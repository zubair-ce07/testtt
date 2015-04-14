'use strict';

var powersuiteApp = angular.module('powersuite', [
  'ngRoute',
  'ngResource',
  'powersuiteControllers',
  'powersuiteServices',
  'ui.bootstrap'
]);

powersuiteApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/search', {
        templateUrl: 'partials/search.html',
        controller: 'SearchCtrl'
      }).
      when('/favourites', {
        templateUrl: 'partials/favourites.html',
        controller: 'FavouritesCtrl'
      }).
      otherwise({
        redirectTo: 'partials/search.html'
      });
  }]);

powersuiteApp.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.useXDomain = true;
  $httpProvider.defaults.withCredentials = true;
  delete $httpProvider.defaults.headers.common["X-Requested-With"];
  $httpProvider.defaults.headers.common["Accept"] = "application/json";
  $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
}
]);
