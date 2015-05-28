ngdocket.controller('SearchCtrl', ['$scope', 'Docket', '$http',
    function ($scope, Docket, $http) {
        $scope.click_dockets = function() {

           $scope.dockets = Docket.get().$promise.then(function(data){
               $scope.dockets = data.dockets;
            });
        };
        $http.get('app/state/state.json').success(function (data) {
            $scope.states = data;
        });
    }
]);

ngdocket.controller('DetailCtrl', ['$scope', 'DocketDetail','$routeParams',
    function ($scope, DocketDetail,$routeParams) {

            var id = $routeParams.id
            $scope.docketsDetail = DocketDetail.get(id).$promise.then(function (data) {
                console.log(data.dockets[0]);
                $scope.docketsDetail = data.dockets[0];
            });
    }
]);

ngdocket.controller('FillingCtrl', ['$scope', 'Filing', '$http',
    function ($scope, Filing, $http) {
        $scope.filing = Filing.get().$promise.then(function (data) {
            console.log(data.dockets);
            $scope.docket = data.dockets[0];
        });
        $scope.values = [{name: 1, id: 1}, {name: 2, id: 2}, {name: 3, id: 3}, {name: 4, id: 4}]
    }
]);