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