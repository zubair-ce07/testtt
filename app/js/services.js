'use strict';

/* Services */

var powersuiteService = angular.module('powersuiteServices', ['ngResource','ngRoute']);

powersuiteService.constant('url', 'http://localhost:3000/');
powersuiteService.constant('apiUrl', 'http://localhost:3000/api/v1');

powersuiteService.factory('User',['$resource', function($resource){
  var user = {email: 'virtouso.irfan@gmail.com', access_token:'CAAH2XfiyuVgBAKoovNarEBLzaN7ZAJKVrcqcqEnJKreLgZC2SoepditLlSX8zmnZAWJ0dCXavdTekZBbAMcP5oLMssJnICoZB6d5MWmR9AHzJDKM7TIJM9ZA0gRIs5ySjqdivyDaT13ZBUxzDgaLnZCZA3q5xt3634TdavBwFqknBd7exKQr0yzsOzh1ikcGT5OYGykIzQZCcfxET1GBZBgclJUqogT4AOP8mZAsOUc52hAwa3nZAF9OSdEpZBfoDiiyPcU8jUPWINnmxfoVbuFrmj4DPL'};
  return user;
}]);

powersuiteService.service('Dockets', function($resource, apiUrl, $http, $q, User){
    this.getSchool = function() {
      return $http.get(apiUrl + '/schools/:1', {access_token: User.access_token, email: User.email});
    }
});

