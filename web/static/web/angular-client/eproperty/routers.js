angular.module('epropertyRouters', ['ngRoute'])

    .config(function ($routeProvider) {

        $routeProvider
            .when('/',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/users/sign_up.html',
                controller: 'signUpController'
            })
            .when('/dashboard',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/customized_search.html',
                controller: 'customizedSearchController'
            })
            .when('/sign-in',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/users/sign_in.html',
                controller: 'signInController'
            })
            .when('/account/profile',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/users/profile.html',
                controller: 'profileController'
            })
            .when('/account/logout',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/users/sign_in.html',
                controller: 'logoutController'
            })
            .when('/account/password/change',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/users/change_password.html',
                controller: 'changePasswordController'
            })
            .when('/posts/all',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/posts.html',
                controller: 'allPostsController'
            })
            .when('/posts/hot',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/posts.html',
                controller: 'hotPostsController'
            })
            .when('/posts/my-posts',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/posts.html',
                controller: 'myPostsController'
            })
            .when('/my-requests',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/requests.html',
                controller: 'myRequestsController'
            })
            .when('/posts/search-results',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/posts.html',
                controller: 'searchResultsController'
            })
            .when('/posts/:postId',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/post_details.html',
                controller: 'postDetailsController'
            })
            .when('/posts/:postId/process-request/:requestId/:status',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/post_details.html',
                controller: 'processRequestController'
            })
            .when('/posts/post/new',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/new_post.html',
                controller: 'newPostController'
            })
            .when('/posts/:postId/request/new',
            {
                templateUrl: 'static/web/angular-client/eproperty/partials/posts/new_request.html',
                controller: 'newRequestController'
            })
            .otherwise({ redirectTo: '/' });
    });