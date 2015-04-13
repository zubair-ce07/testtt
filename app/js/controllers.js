'use strict';

/* Controllers */

var powersuiteControllers = angular.module('powersuiteControllers', []);

powersuiteControllers.controller('SearchCtrl',['$scope','Dockets',
  function($scope, Dockets) {
    $scope.school = Dockets.getSchool;
    $scope.searchDockets = function(dockets){
      console.log(dockets);
      $scope.dockets = {states:10, keyword: "SEARCH", to:'2015-04-10', from:"2015-04-14"};
    }
  }]
);

powersuiteControllers.controller('FavouritesCtrl',
  function($scope) {

  }
);
