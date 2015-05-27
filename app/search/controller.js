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
                console.log(data.dockets);
                $scope.docketsDetail = data.dockets;
            });
    }
]);