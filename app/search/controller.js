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
            $scope.dockets_found='';
            $scope.count = 0;
            $scope.flag = 0;
            getDockets();
        };
        var getDockets = function () {
            $scope.state = [];
            if ($scope.select2states.states) {
                for (var i = 0, len = $scope.select2states.states.length; i < len; i++) {

                    $scope.state[i] = $scope.select2states.states[i].abbreviation;
                }
            }
            console.log($scope.state);
            $scope.docket.state = $scope.state
            $scope.docket.keyword = $scope.keyword;
            $scope.docket.scope = $scope.scope;
            $scope.docket.before = $scope.filingBefore;
            $scope.docket.after = $scope.filingAfter;
            if ($scope.flag != 1) {
                Docket.get($scope.docket.state, $scope.docket.cursor, $scope.docket.keyword, $scope.docket.scope, $scope.docket.before, $scope.docket.after).then(function (resp) {
                    for (var i = 0; i < resp.data.dockets.length; i++) {
                        if (resp.data.metadata.cursor != '' || $scope.flag != 1) {
                            $scope.dockets.push(resp.data.dockets[i]);
                            $scope.count = $scope.count + 1;
                        }
                    }
                    if (resp.data.metadata.cursor == '') {
                        $scope.flag = 1;
                    }
                    $scope.docket.cursor = resp.data.metadata.cursor;
                    $scope.dockets_found = resp.data.metadata.dockets_found;
                    $scope.disable_scroll = false;

                });
            }

        };
        $scope.disable_scroll = false;
        $scope.getNextDockets = function () {
            if ($scope.disable_scroll) {
                return;
            }
            $scope.disable_scroll = true;
            getDockets();

        };



        $http.get('app/state/state.json').success(function (data) {
            $scope.states = data;
        });
    }
]);

ngdocket.controller('DetailCtrl', ['$scope', 'DocketDetail','$routeParams',
    function ($scope, DocketDetail,$routeParams) {

        var id = $routeParams.id;
        $scope.docketsDetail = DocketDetail.get(id).$promise.then(function (data) {
            console.log(data.dockets[0]);
            $scope.docketsDetail = data.dockets[0];
        });
        if ($scope.docketsDetail != null) {
            $scope.showDetails=true
        };



    }
]);

