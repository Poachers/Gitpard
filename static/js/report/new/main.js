gitpard.controller('NewReportCtrl',
    ['$scope', '$API', '$interval', '$loading',
        function ($scope, API, $interval, $loading) {
            $scope.types = [
                {
                    name: 'По разработчику',
                    id: 1
                },
                {
                    name: 'По файлу',
                    id: 2
                }
            ];

            $scope.type = $scope.types[0];

            $scope.getBranches = function () {
                API.reports.get({id: 31}, function (data) {
                    if (data.error) {
                        location.href = '/';
                    }

                    $scope.branches = data.branches;
                    $scope.branch = $scope.branches[0];
                    $scope.include = data.mask.include.join('\n');
                    $scope.exclude = data.mask.exclude.join('\n');
                    $scope.changeParams();
                });
            };

            $scope.changeParams = function () {
                API.reports.tree({
                    id: location.hash.replace('#', ''),
                    branch: $scope.branch.branch_name,
                    mask: {
                        include: $scope.include.split('\n'),
                        exclude: $scope.exclude.split('\n')
                    }
                }, function (data) {
                    function getPath(item, subPath) {
                        for (var c = 0, l = item.length; c < l; c++) {
                            if (item[c].nodes) {
                                getPath(item[c].nodes, (subPath || '') + '/' + item[c].text);
                            } else {
                                $scope.files.push({
                                    path: (subPath || '') + '/' + item[c].text,
                                    color: item[c].color
                                });
                            }
                        }
                    }

                    if (data.project) {
                        $scope.files = [];
                        getPath(data.project);
                    }
                });
            };

            $scope.getReport = function () {
                API.reports.create({
                    id: location.hash.replace('#', ''),
                    branch: $scope.branch.branch_name,
                    kind: $scope.type.id,
                    mask: {
                        include: $scope.include.split('\n'),
                        exclude: $scope.exclude.split('\n')
                    }
                }, function(){
                    location.href = '/report/#?id=' + location.hash.replace('#', '') + '&page=1'
                }, function(){
                    console.log(arguments);
                })
            };

            $scope.getBranches();
        }]);