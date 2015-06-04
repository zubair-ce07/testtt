ngdocket.factory('Docket', function ($http, $resource) {
    var Docket = {
        dockets: [],
        state: [],
        busy: false,
        cursor: '',
        keyword: '',
        scope: '',
        before: '',
        after: '',
        type:'',
        order: '',
        get: function () {
            var url = 'http://aeedocketapi-staging.appspot.com/dockets';
            return $http.get(url,
                {
                    params: {
                        api_key: 'd4dc4045dd431d43b317190a41b982aa',
                        cursor: this.cursor,
                        q: this.keyword,
                        keyword_scope: this.scope,
                        filed_on_before: this.before,
                        filed_on_after: this.after,
                        'states[]': this.state,
                        sort: this.type,
                        direction: this.order,
                        json: 'JSON_CALLBACK'
                    }
                }
            ).success(function (data) {
                });
        }

    };

    return Docket;

});