angular.module('epropertyServices', ['ngResource'])
    //resources related to posts module
    .factory('postAPI', function ($resource) {
        return {
            posts: $resource('/post-api/posts/all/'),
            hot_posts: $resource('/post-api/posts/hot/'),
            my_posts: $resource('/post-api/posts/my-posts/'),
            search_posts: $resource('/post-api/posts/search/'),
            my_requests: $resource('/post-api/my-requests/'),
            post:{
                details: $resource('/post-api/posts/:postId/', {postId: '@postId'}, {
                    get: {method: 'GET'}
                }),
                create:  $resource('/post-api/posts/new\\/', {}, {
                    new: {method: 'POST'}
                }),
                requests:{
                    create: $resource('/post-api/posts/:postId/request/new\\/', {postId: '@postId'}, {
                        new: {method: 'POST'}
                    }),
                    all: $resource('/post-api/posts/:postId/requests/', {postId: '@postId'}),
                    request: $resource('/post-api/posts/:postId/process-request/:requestId\\/', {
                            postId: '@postId',
                            requestId: '@requestId' },
                        {
                            update: {method: 'PUT'}
                        })
                }
            }
        };
    })
    //resources related to users module.
    .factory('userAPI', function ($resource) {
        return {
            auth: $resource('/user-api/login\\/', {}, {
                login: {method: 'POST'}
            }),
            account: $resource('/user-api/logout\\/', {}, {
                logout: {method: 'POST'}
            }),
            users: $resource('/user-api/sign-up\\/', {}, {
                create: {method: 'POST'}
            }),
            profile: $resource('/user-api/account/profile/edit\\/', {}, {
                update: {method: 'PUT'}
            }),
            password: $resource('/user-api/account/password/change\\/', {}, {
                change: {method: 'POST'}
            })
        };
    });