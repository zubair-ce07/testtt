ngdocket.factory('FilingFactory', function ($resource, $http) {
    return {
        getFilings: function (params) {
            var url = 'http://aeedocketapi-staging.appspot.com/dockets/'+params.docket+'/filings';
            var params = {

                api_key: 'd4dc4045dd431d43b317190a41b982aa',
                json: 'JSON_CALLBACK',
                q: params.keyword,
                keyword_scope: params.scope,
                cursor: params.cursor
                //filed_on_before: params.before,
                //filed_on_after: params.after
            };
            var filing = $resource(url, params,
                {get: {method: 'GET'}}
            );
            //$http.get(url, params);
            return filing.get().$promise;
        }
    }
});