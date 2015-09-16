angular.module('userControllers', [])

    .controller('signInController', function ($cookies, $scope, $location, userAPI) {

        $scope.signIn = function (signInForm) {

            if (signInForm.$valid) {
                userAPI.auth.login({
                    email: $scope.email,
                    password: $scope.password
                }).$promise
                    .then(function (data) {

                        $cookies.put('user', JSON.stringify(data));
                        $cookies.put('isAuthenticated', true);
                        $location.path('/dashboard');

                    }).catch(function (data) {
                        // on incorrect username and password
                        if (data.data.message) {
                            alert(data.data.message);
                        }
                        else {
                            alert('Unable to sign in.');
                        }
                    });
            }
        };
    })
    .controller('signUpController', function ($scope, $cookies, $location, $filter, userAPI) {

        if (!$cookies.get('isAuthenticated')) {

            $scope.user = {};
            $scope.user.address = {};
            $scope.signUp = function (signUpForm) {

                if (signUpForm.$valid) {
                    $scope.user.born_on = $filter('date')($scope.born_on, "yyyy-MM-dd");
                    userAPI.users.create($scope.user)
                        .$promise.then(function (data) {
                            $location.path('/sign-in');
                        })
                        .catch(function (data) {
                            if (data.data.password) {
                                alert(data.data.password[0]);
                            }
                            else {
                                alert('Unable to create your account.');
                            }
                        });
                }
            };
        }
        else {
            $location.path('/dashboard');
        }
    })
    .controller('profileController', function ($scope, $location, $cookies, $filter, userAPI) {

        if ($cookies.get('isAuthenticated')) {
            $scope.user = JSON.parse($cookies.get('user'));
            $scope.born_on = new Date($scope.user.born_on);

            $scope.update = function (profileForm) {

                if (profileForm.$valid) {
                    $scope.user.born_on = $filter('date')($scope.born_on, "yyyy-MM-dd");
                    userAPI.profile.update($scope.user)
                        .$promise.then(function (data) {
                            alert("Updated successfully.");
                            $cookies.put('user', JSON.stringify(data));
                        })
                        .catch(function (data) {
                            alert('Error while updating your profile.');
                            $location.path('/dashboard');
                        });
                }
            };
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('changePasswordController', function ($scope, $cookies, $location, userAPI) {

        if ($cookies.get('isAuthenticated')) {

            $scope.updatePassword = function () {
                //$scope.error = false;
                userAPI.password.change($scope.user)
                    .$promise.then(function (data) {
                        $cookies.remove('user');
                        $cookies.remove('isAuthenticated');
                        alert('password has been changed successfully. Please login in again.');
                        $location.path('/sign-in');
                    })
                    .catch(function (data) {
                        if (data.data.non_field_errors) {
                            alert(data.data.non_field_errors[0]);
                        }
                        else if (data.data.new_password) {
                            alert(data.data.new_password[0]);
                        }
                    });
            };
        }
        else {
            $location.path('/sign-up');
        }
    })
    .controller('logoutController', function ($cookies, $route, $location, userAPI) {

        if ($cookies.get('isAuthenticated')) {
            userAPI.account.logout()
                .$promise.then(function () {
                    $cookies.remove('user');
                    $cookies.remove('isAuthenticated');
                    $location.path('/sign-in');
                })
                .catch(function (data) {
                    $cookies.remove('user');
                    $cookies.remove('isAuthenticated');
                    alert('Error while logging you out.Please Sign in again.');
                    $location.url('/sign-in');
                    $route.reload();
                });
        }
        else {
            alert('You are not logged in.');
        }
    });