ngdocket.controller('FillingCtrl', ['$scope', 'Filing', '$routeParams', '$location',
    function ($scope, Filing, $routeParams, $location) {
        var docket_id = $routeParams.docket_id,
            filing_id = $routeParams.filing_id;
        $scope.navigation = 'Filing';
        $scope.filing = Filing.get(docket_id, filing_id).$promise.then(function (data) {
            if (data.error) {
                console.log('Docket not found or filing not found');
            }
            else {
                $scope.docket = data.dockets[0];
            }
            //$scope.docket.filings[0].documents[0].source_url = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/149125/material-design-2.pdf";
            //$scope.docket.filings[0].documents[1].source_url = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/149125/relativity.pdf";
            //$scope.file_url= 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/149125/material-design-2.pdf'
        }, function (reason) {
            $location.path('/index');
        });
        $scope.selected_document_url = false;
        $scope.selected_document = {};
        $scope.$watch('selected_document.document', function () {
            if ($scope.selected_document.document &&
                $scope.selected_document.document.source_url) {
                $scope.selected_document_url = "bower_components/pdf/web/viewer.html?file=" + $scope.selected_document.document.source_url;
            }
        });

    }
]);