'use strict';
var states = [
    { name: 'base', state: { abstract: true, url: '', templateUrl: '/static/forecast/views/base.html', data: {text: "Base", visible: false } } },
    { name: 'query', state: { url: '/query', parent: 'base', templateUrl: '/static/forecast/views/query.html', controller: 'AppCtrl', data: {text: "App", visible: false } } },
    { name: 'result', state: { url: '/result', parent: 'base', templateUrl: '/static/forecast/views/report.html', controller: 'ReportCtrl', data: {text: "Report", visible: false } } }
];

var weatherApp = angular.module('app', ['ui.router', 'ngRoute', 'snap', 'ngAnimate', 'chart.js']);


weatherApp.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $urlRouterProvider.rule(function ($injector, $location) {
        var path = $location.url();

        // check to see if the path has a trailing slash
        if ('/' === path[path.length - 1]) {
            return path.replace(/\/$/, '');
        }

        if (path.indexOf('/?') > -1) {
            return path.replace('/?', '?');
        }

        return false;
    });
    $urlRouterProvider.otherwise('/query');

    angular.forEach(states, function (state) {
        $stateProvider.state(state.name, state.state);
    });

});

weatherApp.controller('AppCtrl', function ($scope, $location, service) {

    $scope.submit = function(){
        $scope.error = false;
        $scope.type = "C"
        if(!$scope.year || !$scope.month){
            $scope.error = true;
        }
        else{
            service.getInfo($scope.type, $scope.year, $scope.month).then(function (report) {
                if (report) {
                    service.transformAndSaveReportForChart(report, $scope.type);
                    $location.path('/result');
                }
                else{
                    alert("Nothing for ya. Run away");
                }
            })
        }
    }
});


weatherApp.controller('ReportCtrl', function($scope, service, $location) {
    var chart = service.chart;
    if(!chart){
        $location.path('/query');
    }

    $scope.labels = chart.labels;
    $scope.series = chart.series;
    $scope.colors = chart.colors;
    $scope.data = chart.data;

    $scope.onHover = function (points, evt) {
        if(points.length){
            $scope.counter = !$scope.counter;
            var audio = new Audio('/static/forecast/audio/'+($scope.counter?1:2)+'.wav');
            audio.play();
        }
    };

    $scope.onClick = function (points, evt) {
        console.log("hey");
    };
});


weatherApp.service('service', ['$http', function ($http) {

    this.transformAndSaveReportForChart = function(report, type){
        var scope = this;
        scope.chart = {}
        if(type == 'C'){
            scope.chart.labels = [];
            scope.chart.series = ['Min Temp', 'Max Temp'];
            scope.chart.colors = ['#00B0FF', '#E57373'];
            scope.chart.data = [[], []];

            report.daily_weathers_info.forEach(function(value, index){
                scope.chart.labels.push(value.day)
                scope.chart.data[0].push(value.min_temp)
                scope.chart.data[1].push(value.max_temp)
            })
        }
    };

    this.getInfo = function (type, year, month) {
        return $http({
            "method": 'GET',
            "url": "/weatherman/weather?type="+type+"&year="+year+"&month="+month,
            "dataType": "Json"
        }).then(function (res) {
            if (typeof (res) != 'undefined' && typeof(res.status) != 'undefined' && res.status == 200 && res.data) {
                return JSON.parse(res.data);
            }
            return false;
        }
        )
    };
}]);