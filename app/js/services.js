'use strict';

/* Services */

var powersuiteService = angular.module('powersuiteServices', ['ngResource']);

powersuiteService.constant('url','');
powersuiteService.constant('apiUrl','');

powersuiteService.factory('Search', ['$resource',
  function($resource) {
    return $resource('phones/:phoneId.json', {}, {
      query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
    });
  }]);
