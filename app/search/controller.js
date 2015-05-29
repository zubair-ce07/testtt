ngdocket.controller('SearchCtrl', ['$scope', 'Docket', '$http',
    function ($scope, Docket, $http) {
        $scope.states = []
        $scope.select2states = {};
        //    $scope.click_dockets = function() {
        //
        //       $scope.dockets = Docket.get().$promise.then(function(data){
        //           $scope.dockets = data.dockets;
        //        });
        //    };


        $scope.docket = Docket;
        $scope.dockets = [];
        var getDockets = function () {
            Docket.get($scope.docket.cursor).then(function (resp) {
                for (var i = 0; i < resp.data.dockets.length; i++) {
                    $scope.dockets.push(resp.data.dockets[i]);
                }
                $scope.docket.cursor= resp.data.metadata.cursor;
                $scope.disable_scoll = false;
            });
        };
        $scope.disable_scoll = false;
        $scope.getNextDockets = function () {
            if ($scope.disable_scoll) {
                return;
            }
            getDockets();
            $scope.disable_scoll = true;
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

