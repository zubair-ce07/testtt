var ngdocket = angular.module('ngdocket', ['ngResource', 'ngRoute']);

ngdocket.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
        when('/search',
        {
            templateUrl: 'app/search/partials/search.html',
            controller: 'SearchCtrl'
            //activetab: 'manage'
        }).
        when('/dockets/:id',
        {
            templateUrl: 'app/search/partials/docket_details.html',
            controller: 'DetailCtrl'
            //activetab: 'manage'
        }).
        otherwise({redirectTo: '/index.html'})
}
]);