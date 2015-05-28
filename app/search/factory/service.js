ngdocket.factory('Docket', ['$resource', function($resource) {
    function Docket() {
        this.service = $resource('http://aeedocketapi-staging.appspot.com/dockets?api_key=d4dc4045dd431d43b317190a41b982aa',
            {
                callback: "JSON_CALLBACK"
            }
        );
    };
    Docket.prototype.get = function(){
        return this.service.get();
    }
    return new Docket;
}]);

ngdocket.factory('Filing', ['$resource', function ($resource) {
    function Filing() {
        this.service = $resource('http://aeedocketapi-staging.appspot.com/dockets/4503923427639296/filings/5348024557502464?api_key=d4dc4045dd431d43b317190a41b982aa',
            {
                callback: "JSON_CALLBACK"
            }
        );
    }

    Filing.prototype.get = function () {
        return this.service.get();
    };
    return new Filing;
}]);
