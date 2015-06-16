ngdocket.factory('Poll', function ($resource, $http) {
    return {
        getPollDocket: function (params) {
            var url = 'http://polling.pucscrape.appspot.com/dockets/searchpollresults/'+params.poll_id;
            var params = {
                        page: params.page,
                        json: 'JSON_CALLBACK'
            };
            var polling = $resource(url, params,
                {get: {method: 'GET'}}
            );
            return polling.get().$promise;
        }
    }
});