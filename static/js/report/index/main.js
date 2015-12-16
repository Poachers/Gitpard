gitpard.controller('ReportIndexCtrl',
    ['$scope', '$location', '$loading', '$interval', '$API',
        function ($scope, $location, $loading, $interval, API) {
            function getPage() {
                if (
                    typeof $location.search().page !== 'number' ||
                    $location.search().page < 1 ||
                    parseInt($location.search().page) != $location.search().page
                ) {
                    $location.search('page', 1);
                }

                return $location.search().page;
            }

            $scope.getRepoId = function () {
                console.log($location.hash());
                if (!$location.search().id) {
                    debugger;
                    location.href = '/';
                }
                return $location.search().id;
            };
            $scope.getRepoId();

            function reportsGet() {
                API.reports.get({id: $scope.getRepoId(), page: getPage()}, function successCallback(data) {
                    $scope.reports = data.reports.reverse();
                    console.log(data);
                });
            }

            $scope.reportView = function (report) {
                location.href = '/report/view/#?repo=' + report.repository + '&id=' + report.id;
            };

            reportsGet();
        }]);