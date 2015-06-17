ngdocket.controller('SearchCtrl', ['$scope', 'Docket','Polling','Poll' , '$http', '$route',
    function ($scope, Docket, Polling, Poll, $http, $route) {
        $scope.keyword='';
        $scope.scope = '';
        $scope.filingBefore = '';
        $scope.filingAfter = '';
        $scope.type = '';
        $scope.order = '';
        $scope.states = [];
        $scope.select2states = {};
        $scope.navigation = 'DOCKETS';
        $scope.polling_id ='';
        $scope.page = 0;
        $scope.more = true;
        $scope.mark= false;


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

            $scope.docket.state = $scope.state;
            $scope.docket.keyword = $scope.keyword;
            $scope.docket.scope = $scope.scope;
            $scope.docket.before = $scope.filingBefore;
            $scope.docket.after = $scope.filingAfter;
            $scope.docket.type = $scope.type;
            $scope.docket.order = $scope.order;

            if ($scope.flag != 1) {
                if ($scope.scope == 'all' && !$scope.polling_id && $scope.page == 0 && ($scope.keyword && $scope.keyword.length > 2)) {

                    Polling.getPollId(
                        {
                            state: $scope.state,
                            keyword: $scope.keyword,
                            scope : $scope.scope,
                            before : $scope.filingBefore,
                            after : $scope.filingAfter,
                            type : $scope.type,
                            order : $scope.order
                        }

                    ).then(function (resp) {
                            $scope.polling_id = resp.poll_id;
                            if($scope.polling_id.length>1) {
                                $scope.page = 1;
                            }
                            $scope.disable_scroll = false;
                            getDockets();
                        });


                }else if($scope.polling_id.length>1){

                    Poll.getPollDocket({
                            page: $scope.page,
                            poll_id: $scope.polling_id
                        }
                    ).then(function (resp) {

                            for (var i = 0; i < resp.dockets.length; i++) {
                                if (resp.metadata.more ==false && $scope.mark == false){
                                    $scope.dockets = [];
                                    $scope.mark= true;
                                }
                                if ($scope.flag != 1) {
                                    $scope.dockets.push(resp.dockets[i]);

                                }

                            }

                            if (Math.ceil(resp.metadata.count/30) == $scope.page) {
                                $scope.flag = 1;
                            }

                            $scope.page = resp.metadata.page + 1;
                            $scope.more = resp.metadata.more;
                            $scope.dockets_found = resp.metadata.count;
                            $scope.disable_scroll = false;
                        });

                } else {
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
            } else
            {
                $scope.page = 1;
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

        $scope.clearForm = function() {
            $scope.keyword='';
            $scope.scope = '';
            $scope.filingBefore = '';
            $scope.filingAfter = '';
            $scope.type = '';
            $scope.order = '';
            $scope.states = [];
            $scope.select2states = {};
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
        $scope.navigation = 'DOCKETS';

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

         $scope.cleanForm = function() {
            $scope.keyword='';
            $scope.scope = '';
            $scope.before = '';
            $scope.after = '';
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

