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
                    $scope.reports = data.reports;
                    console.log(data);
                });
            }

            reportsGet();
            $interval(function () {
                console.log(1);
                $loading(false);
            }, 1e5);
        }]);