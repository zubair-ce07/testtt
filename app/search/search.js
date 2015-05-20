var searchDocket = angular.module('searchDocket', []);
searchDocket.controller('SearchCtrl', ['$scope','$location', '$http', function (scope, http){
    http.get('http://pucscrape.appspot.com/').success(function(data) {
        scope.dockets = data;
    });
}]);



