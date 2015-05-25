ngdocket.controller('SearchCtrl', ['$scope','Docket',
    function($scope, Docket){
        $scope.click_dockets = function() {

           $scope.dockets = Docket.get().$promise.then(function(data){
               console.log(data.dockets);
               $scope.dockets = data.dockets;
            });
        };
    }
]);
