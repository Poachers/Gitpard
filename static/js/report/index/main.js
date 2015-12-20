gitpard.controller('ReportIndexCtrl',
    ['$scope', '$location', '$loading', '$interval', '$API', '$timeout',
        function ($scope, $location, $loading, $interval, API, $timeout) {
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

            var api = {
                reportsGet: function successCallback(data) {
                    if (data.error) {
                        $loading();
                        $timeout(function () {
                            API.reports.get({id: $scope.getRepoId(), page: getPage()}, api.reportsGet, function () {
                            }, {alert: false, loading: true});
                        }, 1e3);
                    } else {
                        $scope.reports = data.reports.reverse();
                    }
                }
            };

            function reportsGet() {
                API.reports.get({id: $scope.getRepoId(), page: getPage()}, api.reportsGet);
            }

            $scope.reportView = function (report) {
                if ([1].indexOf(report.state) == -1) {
                    return false;
                }
                location.href = '/report/view/#?repo=' + report.repository + '&id=' + report.id;
            };

            $scope.reportDelete = function (report) {
                if ([-1, 1].indexOf(report.state) == -1) {
                    return;
                }
                API.reports.delete(report, function (data) {
                    if (!data.error) {
                        api.reportsGet({error: true});
                    }
                });
            };

            reportsGet();
        }]);