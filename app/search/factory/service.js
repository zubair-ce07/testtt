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



ngdocket.factory('Reddit', function($http) {
  var Reddit = {
    dockets : [],
    busy : false,
    cursor : '',
    get : function() {
        
        var url = 'http://aeedocketapi-staging.appspot.com/dockets?api_key=d4dc4045dd431d43b317190a41b982aa&cursor=' + this.cursor + '&json=JSON_CALLBACK"';
        return $http.get(url).success(function(data) {

        });
    }
  };

  return Reddit;

});