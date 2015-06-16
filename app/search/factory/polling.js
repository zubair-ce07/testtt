ngdocket.factory('Polling', function ($resource, $http) {
    return {
        getPollId: function (params) {
            var url = 'http://polling.pucscrape.appspot.com/dockets';
            var params = {
                        q: params.keyword,
                        keyword_scope: params.scope,
                        filed_on_before: params.before,
                        filed_on_after: params.after,
                        'states[]': params.state,
                        sort: params.type,
                        direction: params.order,
                        json: 'JSON_CALLBACK'

            };
            var polling = $resource(url, params,
                {get: {method: 'GET'}}
            );
            return polling.get().$promise;
        }
    }
});