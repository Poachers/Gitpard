gitpard.controller('ReportViewCtrl',
    ['$scope', '$location', '$loading', '$interval', '$API',
        function ($scope, $location, $loading, $interval, API) {
            API.reports.view($location.search(), function (data) {
                $scope.sort = '-result';
                $scope.report = data;
                $scope.report.mask.include = $scope.report.mask.include.join('\n');
                $scope.report.mask.exclude = $scope.report.mask.exclude.join('\n');

                $scope.togglSort = function (key) {
                    if ($scope.sort == key) {
                        $scope.sort = '-' + key;
                    } else if ($scope.sort == '-' + key) {
                        $scope.sort = '';
                    } else {
                        $scope.sort = key;
                    }
                    console.log($scope.sort)
                };
            });
        }]);