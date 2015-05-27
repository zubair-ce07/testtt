ngdocket.factory('DocketDetail', ['$resource', function($resource) {
    function DocketDetail() {
        this.service = $resource('http://aeedocketapi-staging.appspot.com/dockets/:id?api_key=d4dc4045dd431d43b317190a41b982aa',
            {
                callback: "JSON_CALLBACK", id: '@id'
            }
        );
    };
    DocketDetail.prototype.get = function(DocketId){
        return this.service.get({id: DocketId});
    }
    return new DocketDetail;
}]);