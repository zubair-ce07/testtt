angular.module('postControllers', [])

    .controller('allPostsController', function ($scope, $cookies, $location, postAPI) {

        if ($cookies.get('isAuthenticated')) {
            $scope.posts = postAPI.posts.query()
                .$promise.then(function (data) {
                    $scope.posts = data;
                }).catch(function (data) {
                    alert('Error fetching posts.');
                });
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('myPostsController', function ($scope, $location, $cookies, postAPI) {

        if ($cookies.get('isAuthenticated')) {

            $scope.posts = postAPI.my_posts.query()
                .$promise.then(function (data) {
                    $scope.posts = data;
                }).catch(function (data) {
                    alert(JSON.stringify(data));
                });
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('myRequestsController', function ($scope, $location, $cookies, postAPI) {

        if ($cookies.get('isAuthenticated')) {

            $scope.posts = postAPI.my_requests.query()
                .$promise.then(function (data) {
                    $scope.requests = data;
                }).catch(function (data) {
                    alert(JSON.stringify(data));
                });
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('postDetailsController', function ($scope, $location, $cookies, $routeParams, postAPI) {

        if ($cookies.get('isAuthenticated')) {

            postAPI.post.details.get({postId: $routeParams.postId})
                .$promise.then(function (data) {
                    $scope.post = data;
                    $scope.user = JSON.parse($cookies.get('user'));
                    postAPI.post.requests.all.query({postId: $routeParams.postId})
                        .$promise.then(function (data) {
                            $scope.requests = data;
                        }).catch(function (data) {
                            alert('failed to get requests');
                            $scope.post.title = JSON.stringify(data);
                        })

                }).catch(function (data) {
                    alert('failed to get posts');
                });
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('processRequestController', function ($scope, $cookies, $location, $routeParams, postAPI) {

        if ($cookies.get('isAuthenticated')) {

            var request = {status: $routeParams.status};
            postAPI.post.requests.request.update({
                postId: $routeParams.postId,
                requestId: $routeParams.requestId
            }, request).$promise
                .then(function (data) {
                    $location.path('/posts/' + $routeParams.postId);
                })
                .catch(function (data) {
                    alert('failed to update request.');
                });
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('newPostController', function ($scope, $cookies, $filter, $location, postAPI) {

        if ($cookies.get('isAuthenticated')) {

            $scope.kinds = [
                {index: 'house', value: 'House'},
                {index: 'plot', value: 'Plot'},
                {index: 'commercial_plot', value: 'Commercial Plot'},
                {index: 'commercial_building', value: 'Commercial Building'},
                {index: 'flat', value: 'Flat'},
                {index: 'shop', value: 'Shop'},
                {index: 'farm_house', value: 'Farm House'}
            ];

            $scope.createPost = function (newPostForm) {

                if (newPostForm.$valid) {
                    var expired_on = $filter('date')($scope.expired_on, "yyyy-MM-dd'T'HH:mm:ssZ");
                    $scope.post.expired_on = expired_on.substring(0, 18) + ".000000" + expired_on.substring(18, expired_on.length);

                    postAPI.post.create.new($scope.post)
                        .$promise
                        .then(function (data) {
                            $location.path('/posts/my-posts');
                        }).catch(function (data) {

                            if (data.data.title) {
                                alert(data.data.title[0]);
                            }
                            else if (data.data.area) {
                                alert(data.data.area[0]);
                            }
                            else if (data.data.expired_on) {
                                alert(data.data.expired_on[0]);
                            }
                            else if (data.data.demand) {
                                alert(data.data.demand[0]);
                            }
                            else {
                                alert('failed to post new Ad');
                            }
                        });
                }
            };
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('newRequestController', function ($scope, $cookies, $location, $routeParams, postAPI) {

        if ($cookies.get('isAuthenticated')) {

            $scope.createRequest = function (newRequestForm) {

                if (newRequestForm.$valid) {
                    postAPI.post.requests.create.new({postId: $routeParams.postId}, $scope.request)
                        .$promise
                        .then(function (data) {
                            $location.path('/my-requests');
                        }).catch(function () {
                            if (data.data.requested_price) {
                                alert(data.data.requested_price[0]);
                            }
                            else {
                                alert('failed to post new request');
                            }
                        });
                }
            };

        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('customizedSearchController', function ($scope, $rootScope, $location, $cookies, postAPI) {

        $scope.kinds = [
            {index: 'house', value: 'House'},
            {index: 'plot', value: 'Plot'},
            {index: 'commercial_plot', value: 'Commercial Plot'},
            {index: 'commercial_building', value: 'Commercial Building'},
            {index: 'flat', value: 'Flat'},
            {index: 'shop', value: 'Shop'},
            {index: 'farm_house', value: 'Farm House'}
        ];

        if ($cookies.get('isAuthenticated')) {

            $scope.search = function () {
                postAPI.search_posts.query($scope.filterCriteria)
                    .$promise
                    .then(function (data) {
                        $rootScope.posts = data;
                        $location.path('/posts/search-results');
                    }).catch(function (data) {
                        alert(JSON.stringify(data));
                        alert('Something went wrong..');
                    });
            }
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('searchResultsController', function ($scope, $rootScope, $location, $cookies) {
        if ($cookies.get('isAuthenticated')) {
            $scope.posts = $rootScope.posts;
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('hotPostsController', function ($scope, $location, $cookies, postAPI) {

        if ($cookies.get('isAuthenticated')) {
            $scope.posts = postAPI.hot_posts.query()
                .$promise.then(function (data) {
                    $scope.posts = data;
                }).catch(function (data) {
                    alert('Error fetching posts.');
                });
        }
        else {
            $location.path('/sign-up');
        }
    });


