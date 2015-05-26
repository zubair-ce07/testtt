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

ngdocket.controller('StateCtrl', ['$scope','$http', function($scope, $http)
		{
			$http.get('app/state/state.json').success (function(data){
				$scope.states = data;
		});

		}

]);