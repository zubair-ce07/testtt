//ngdocket.factory('Docket', ['$resource', function($resource) {
//    function Docket() {
//        this.service = $resource('http://aeedocketapi-staging.appspot.com/dockets?api_key=d4dc4045dd431d43b317190a41b982aa',
//            {
//                callback: "JSON_CALLBACK"
//            }
//        );
//    };
//    Docket.prototype.get = function(){
//        return this.service.get();
//    }
//    return new Docket;
//}]);

ngdocket.factory('Docket', function($http) {
    var Docket = {
        dockets : [],
        state:[],
        busy : false,
        cursor : '',
        keyword : '',
        scope: '',
        before:'',
        after: '',
        get : function() {
            var url = 'http://aeedocketapi-staging.appspot.com/dockets?api_key=d4dc4045dd431d43b317190a41b982aa&cursor='
                + this.cursor + '&q='+this.keyword+'&keyword_scope=' +this.scope+'&filed_on_before='+this.before+
                '&filed_on_after='+this.after+'&states[]=' +this.state+ '&json=JSON_CALLBACK';
            console.log(url);
            return $http.get(url).success(function(data) {

            });
        }
    };

    return Docket;

});