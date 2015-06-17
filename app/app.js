var ngdocket = angular.module('ngdocket', ['ngResource', 'ngRoute', 'infinite-scroll', 'ui.select', 'ngSanitize','720kb.datepicker']);

ngdocket.config(['$routeProvider', '$httpProvider', function ($routeProvider, $httpProvider) {
            $httpProvider.defaults.stripTrailingSlashes = false;

    $routeProvider.
        when('/search',
        {
            templateUrl: 'app/search/partials/search.html',
            controller: 'SearchCtrl'
            //activetab: 'manage'
        }).when('/dockets/:docket_id/filings/:filing_id',
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
        when('/',
        {
            templateUrl: 'app/search/partials/search.html',
            controller: 'SearchCtrl'
        }).
        when('/404',
        {
            templateUrl: 'app/404/partials/view.html'
            //activetab: 'manage'
        }).
        otherwise({redirectTo: '/404'})
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
            out = items;
        }

        return out;
    }
});
