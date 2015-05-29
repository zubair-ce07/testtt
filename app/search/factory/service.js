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

ngdocket.factory('Reddit', function ($http) {
    var Reddit = {
        dockets: [],
        busy: false,
        cursor: '',
        get: function () {
            /*if (this.busy) return;
             this.busy = true;*/

            var url = 'http://aeedocketapi-staging.appspot.com/dockets?api_key=d4dc4045dd431d43b317190a41b982aa&cursor=' + this.cursor + '&json=JSON_CALLBACK"';
            return $http.get(url).success(function (data) {
                /*var items = data.dockets;
                 for (var i = 0; i < items.length; i++) {
                 this.dockets.push(items[i]);
                 }
                 this.cursor = data.metadata.cursor;
                 this.busy = false;*/
            });
    }
    };
<<<<<<< HEAD

    return Reddit;
=======
    return new Filing;
}]);


ngdocket.factory('Reddit', function($http) {
  var Reddit = {
    dockets : [],
    busy : false,
    cursor : '',
    get : function() {
        /*if (this.busy) return;
        this.busy = true;*/

        var url = 'http://aeedocketapi-staging.appspot.com/dockets?api_key=d4dc4045dd431d43b317190a41b982aa&cursor=' + this.cursor + '&json=JSON_CALLBACK"';
        return $http.get(url).success(function(data) {
          /*var items = data.dockets;
          for (var i = 0; i < items.length; i++) {
            this.dockets.push(items[i]);
          }
          this.cursor = data.metadata.cursor;
          this.busy = false;*/
        });
    }
  };

  return Reddit;
>>>>>>> 6dea22f805082b9f28f435b83e6ba924a8287958
});