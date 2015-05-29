ngdocket.controller('SearchCtrl', ['$scope', 'Docket', '$http','Reddit',
    function ($scope, Docket, $http, Reddit) {
        //    $scope.click_dockets = function() {
        //
        //       $scope.dockets = Docket.get().$promise.then(function(data){
        //           $scope.dockets = data.dockets;
        //        });
        //    };


        $scope.reddit = Reddit;

        //Reddit.get();*/
        $scope.dockets = [];
        var getDockets = function(){
            Reddit.get($scope.reddit.cursor).then(function(resp){
                //$scope.dockets = resp.data.dockets;//loop throught response dockets and add them at the end of array.. $scope.dockets.push(resp[i])
                for (var i = 0; i < resp.data.dockets.length; i++) {
                    $scope.dockets.push(resp.data.dockets[i]);
                }
                $scope.reddit.cursor= resp.data.metadata.cursor;//loop throught response dockets and add them at the end of array.. $scope.dockets.push(resp[i])
                //set cursor from response
                $scope.disable_scoll = false;
            });
        };
        //getDockets();
        $scope.disable_scoll = false;

        $scope.getNextDockets = function(){
            if($scope.disable_scoll){
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


ngdocket.controller('DemoController',['$scope','Reddit',  function($scope, Reddit) {

}]);


ngdocket.controller('FillingCtrl', ['$scope', 'Filing', '$http',
    function ($scope, Filing, $http) {
        $scope.filing = Filing.get().$promise.then(function (data) {
            console.log(data.dockets);
            $scope.docket = data.dockets[0];
        });
        $scope.values = [{name: 1, id: 1}, {name: 2, id: 2}, {name: 3, id: 3}, {name: 4, id: 4}]
    }
]);