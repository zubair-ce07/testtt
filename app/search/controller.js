ngdocket.controller('SearchCtrl', ['$scope', 'Docket', '$http',
    function ($scope, Docket, $http) {
        $scope.click_dockets = function() {

           $scope.dockets = Docket.get().$promise.then(function(data){
               console.log(data.dockets);
               $scope.dockets = data.dockets;
            });
        };
        $http.get('app/state/state.json').success(function (data) {
            $scope.states = data;
        });
    }
]);