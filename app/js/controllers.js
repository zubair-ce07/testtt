'use strict';

/* Controllers */

var powersuiteControllers = angular.module('powersuiteControllers', []);

powersuiteControllers.controller('SearchCtrl', ['$scope', '$http', '$filter', 'apiUrl', 'User', 'Dockets',
        function ($scope, $http, $filter, apiUrl, User, Dockets) {





            $scope.searchDockets = function (dockets) {
                Dockets.getSchool().then(function(response){
                    $scope.school = response.data;
                    var orderBy = $filter('orderBy');
                    $scope.friends = [
                        { name: 'John',    phone: '555-1212',    age: 10 },
                        { name: 'Mary',    phone: '555-9876',    age: 19 },
                        { name: 'Mike',    phone: '555-4321',    age: 21 },
                        { name: 'Adam',    phone: '555-5678',    age: 35 },
                        { name: 'Julie',   phone: '555-8765',    age: 29 }
                    ];
                    $scope.order = function(predicate, reverse) {
                        $scope.friends = orderBy($scope.friends, predicate, reverse);
                    };
                    $scope.order('-age',false);
                    console.log($scope.school);
                });
                Dockets.getDockets().then(function(response){
                    $scope.dockets = response.data;
                    console.log($scope.dockets);
                });
                //$scope.dockets = Dockets.getDockets;
                //$scope.school = $http({method: 'GET', url: apiUrl + '/schools/1', params: {access_token: User.access_token, email: User.email}});
                //$scope.dockets = {
                //    state: 10,
                //    word: "SEARCH",
                //    to_date: new Date(2015, 3, 12),
                //    from_date: new Date(2015, 3, 15)
                //};
            }
        }]
);

powersuiteControllers.controller('FavouritesCtrl',
    function ($scope) {

    }
);

powersuiteControllers.controller('DatePickerCtrl', function ($scope) {
    $scope.today = function () {
        $scope.to_date = new Date();
        $scope.from_date = new Date();
    };
    $scope.today();

    $scope.clear = function () {
        $scope.to_date = null;
        $scope.from_date = null;
    };

    // Disable weekend selection
    $scope.disabled = function (date, mode) {
        return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
    };

    $scope.toggleMin = function () {
        $scope.minDate = $scope.minDate ? null : new Date();
    };
    $scope.toggleMin();

    $scope.open = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[0];
});

