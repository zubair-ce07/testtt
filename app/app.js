var ngdocket = angular.module('ngdocket', ['ngResource', 'ngRoute']);

ngdocket.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
        when('/search',
        {
            templateUrl: 'app/search/partials/search.html',
            controller: 'SearchCtrl'
            //activetab: 'manage'
        }).
        otherwise({redirectTo: '/index.html'})
}
]);