ngdocket.controller('SearchCtrl', ['$scope', 'Docket', '$http',
    function ($scope, Docket, $http) {
        $scope.keyword='';
        $scope.scope = '';
        $scope.filingBefore = '';
        $scope.filingAfter = '';
        $scope.type = '';
        $scope.order = '';
        $scope.states = [];
        $scope.select2states = {};
        $scope.navigation = 'Search';

        $scope.click_dockets = function() {
            $scope.docket = Docket;
            $scope.dockets = [];
            $scope.dockets_found='';
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
            $scope.docket.state = $scope.state;
            $scope.docket.keyword = $scope.keyword;
            $scope.docket.scope = $scope.scope;
            $scope.docket.before = $scope.filingBefore;
            $scope.docket.after = $scope.filingAfter;
            $scope.docket.type = $scope.type;
            $scope.docket.order = $scope.order;
            if ($scope.flag != 1) {
                Docket.get(
                    $scope.docket.state,
                    $scope.docket.cursor,
                    $scope.docket.keyword,
                    $scope.docket.scope,
                    $scope.docket.before,
                    $scope.docket.after,
                    $scope.docket.type,
                    $scope.docket.order
                ).then(function (resp) {
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

ngdocket.controller('DetailCtrl', ['$scope','FilingFactory', 'DocketDetail','Filing','$routeParams',
    function ($scope, FilingFactory, DocketDetail, Filing ,$routeParams) {
        $scope.keyword='';
        $scope.scope = '';
        $scope.filings= [];
        $scope.before = '';
        $scope.after = '';
        $scope.showDetails = false;
        $scope.navigation = 'Docket';

        var id = $routeParams.id;

        $scope.docketsDetail = DocketDetail.get(id).$promise.then(function (data) {
            $scope.docketsDetail = data.dockets[0];
            $scope.filings = $scope.docketsDetail.filings;
            $scope.filings_found = $scope.docketsDetail.filings.length;

        });

        if ($scope.docketsDetail != null) {
            $scope.showDetails=true
        }

        $scope.click_filings = function() {
            $scope.filing = Filing;
            $scope.filings = [];
            $scope.filings_found='';
            $scope.flag = 0;
            getFilings();
        };

        var getFilings = function () {
            if ($scope.flag != 1) {
                FilingFactory.getFilings({
                    keyword : $scope.keyword,
                    scope : $scope.scope,
                    before : $scope.before,
                    after : $scope.after,
                    docket : id,
                    cursor : $scope.cursor
                })
                    .then(function (resp) {
                    for (var i = 0; i < resp.dockets[0].filings.length; i++) {
                        if (resp.metadata.cursor != '' || $scope.flag != 1) {
                            $scope.filings.push(resp.dockets[0].filings[i]);
                            $scope.count = $scope.count + 1;
                        }
                    }
                    if (resp.metadata.cursor == '') {
                        $scope.flag = 1;
                    }
                    $scope.cursor = resp.metadata.cursor;
                    $scope.filings_found = resp.metadata.documents_found;
                    $scope.disable_scroll = false;
                    $scope.disable_click = false;

                });
            }

        };

        $scope.disable_scroll = false;
        $scope.disable_click = true;
        $scope.getNextFilings = function () {

            if ($scope.disable_scroll || $scope.disable_click) {
                return;
            }
            $scope.disable_scroll = true;
            getFilings();

        };


    }
]);

