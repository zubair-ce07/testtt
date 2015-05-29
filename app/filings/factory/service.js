ngdocket.factory('Filing', ['$resource', function ($resource) {
    function Filing() {
        this.service = $resource('http://aeedocketapi-staging.appspot.com/dockets/:docket_id/filings/:filing_id?api_key=d4dc4045dd431d43b317190a41b982aa',
            {
                callback: "JSON_CALLBACK", docket_id: '@docket_id', filing_id: '@filing_id'
            }
        );
    }

    Filing.prototype.get = function (docket_id, filing_id) {
        return this.service.get({docket_id: docket_id, filing_id: filing_id});
    };
    return new Filing;
}]);