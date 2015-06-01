ngdocket.controller('SearchCtrl', ['$scope', 'Docket', '$http',
    function ($scope, Docket, $http) {
        $scope.keyword='';
        $scope.scope = '';
        $scope.filingBefore = '';
        $scope.filingAfter = '';
        $scope.states = [];
        $scope.select2states = {};



        //    $scope.click_dockets = function() {
        //
        //       $scope.dockets = Docket.get().$promise.then(function(data){
        //           $scope.dockets = data.dockets;
        //        });
        //    };

        $scope.click_dockets = function() {
            $scope.docket = Docket;
            $scope.dockets = [];


            var getDockets = function () {
                $scope.state= [];
                if ($scope.select2states.states)
                {
                    for (var i = 0, len = $scope.select2states.states.length; i < len; i++) {

                        $scope.state[i] = $scope.select2states.states[i].abbreviation;
                    }
                }
                console.log($scope.state);
                $scope.docket.state = $scope.state
                $scope.docket.keyword =  $scope.keyword;
                $scope.docket.scope =  $scope.scope;
                $scope.docket.before =  $scope.filingBefore;
                $scope.docket.after =  $scope.filingAfter;
                Docket.get($scope.docket.state, $scope.docket.cursor, $scope.docket.keyword,$scope.docket.scope,$scope.docket.before, $scope.docket.after).then(function (resp) {
                    for (var i = 0; i < resp.data.dockets.length; i++) {
                        $scope.dockets.push(resp.data.dockets[i]);
                    }
                    $scope.docket.cursor = resp.data.metadata.cursor;
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
        if ($scope.docketsDetail != null) {
            $scope.showDetails=true
        };

    }
]);

