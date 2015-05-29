<<<<<<< HEAD
var ngdocket = angular.module('ngdocket', ['ngResource', 'ngRoute', 'infinite-scroll', 'ui.select', 'ngSanitize']);
=======
var ngdocket = angular.module('ngdocket', ['ngResource', 'ngRoute','infinite-scroll']);
>>>>>>> 6dea22f805082b9f28f435b83e6ba924a8287958

ngdocket.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
        when('/search',
        {
            templateUrl: 'app/search/partials/search.html',
            controller: 'SearchCtrl'
            //activetab: 'manage'
        }).when('/dockets/:id/filings/:id',
        {
            templateUrl: 'app/filings/partials/view.html',
            controller: 'FillingCtrl'
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


ngdocket.filter('propsFilter', function () {
    return function (items, props) {
        var out = [];

        if (angular.isArray(items)) {
            items.forEach(function (item) {
                var itemMatches = false;

                var keys = Object.keys(props);
                for (var i = 0; i < keys.length; i++) {
                    var prop = keys[i];
                    var text = props[prop].toLowerCase();
                    if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
                        itemMatches = true;
                        break;
                    }
                }
                if (itemMatches) {
                    out.push(item);
                }
            });
        } else {
            // Let the output be the input untouched
            out = items;
        }

        return out;
    }
});
