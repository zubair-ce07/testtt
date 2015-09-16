angular.module('eproperty', ['ngCookies', 'epropertyRouters', 'epropertyServices', 'userControllers', 'postControllers'])

    .config(function ($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    })
    .controller('epropertyController', function ($scope, $cookies, $rootScope, $location) {

        $rootScope.isAuthenticated = $cookies.get('isAuthenticated');
        if ($rootScope.isAuthenticated){
           $location.path('/dashboard');
        }
    });