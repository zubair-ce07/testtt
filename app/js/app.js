'use strict';

var powersuiteApp = angular.module('powersuite', [
    'ngRoute',
    'ngResource',
    'powersuiteControllers',
    'powersuiteServices',
    'ui.bootstrap',
    'ui.router',
    'ui.bootstrap',
    'ui.bootstrap.tpls',
    'ngGrid'
]);
//
//powersuiteApp.config(['$routeProvider',
//  function($routeProvider) {
//    $routeProvider.
//      when('/search', {
//        templateUrl: 'partials/search.html',
//        controller: 'SearchCtrl'
//      }).
//      when('/favorites', {
//        templateUrl: 'partials/favourites.html',
//        controller: 'FavouritesCtrl'
//      }).
//      otherwise({
//        templateUrl: 'partials/home.html'
//      });
//  }]);

powersuiteApp.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state('search', {
            url: '/search',
            templateUrl: 'partials/search.html',
            controller: 'SearchCtrl'
        }).state('favorites', {
            url: '/favorites',
            templateUrl: 'partials/favourites.html',
            controller: 'FavouritesCtrl'
        }).state('home',{
            url:'/home',
            templateUrl: 'partials/home.html'
        })
}]);

powersuiteApp.config(['$httpProvider', function ($httpProvider) {
    delete $httpProvider.defaults.headers.common["X-Requested-With"];
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.withCredentials = true;
    $httpProvider.defaults.headers.common["Accept"] = "application/json";
    $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
}
]);
