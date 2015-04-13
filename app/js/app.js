'use strict';

var powersuiteApp = angular.module('powersuite', [
  'ngRoute',
  'powersuiteControllers',
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
