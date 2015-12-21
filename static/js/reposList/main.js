gitpard.controller('reposListCtrl',
    ['$scope', '$location', '$interval', '$API', '$alert', '$uibModal',
        function ($scope, $location, $interval, API, $alert, $modal) {

            $scope.error = {};

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

            function reposGet() {
                API.repos.get({page: getPage()}, function successCallback(data) {
                    $scope.repos = data.results;
                });
            }

            $scope.changeShowLog = function (repo) {
                if ($scope.showLog == repo.id) {
                    $scope.showLog = undefined;
                } else {
                    if (repo.log) {
                        $scope.showLog = repo.id;
                    }
                }
            };

            $scope.changeUrl = function (url, repo) {
                if ((([2, 4].indexOf(repo.state) != -1 && url == '/report/') || ([2].indexOf(repo.state) != -1 && url == '/analysis/')) && !repo.disable) {
                    location.href = url + '#?id=' + repo.id;
                }
            };

            reposGet();

            $interval(function () {
                reposGet();
            }, 5e3);

            $scope.repoClone = function (repo) {
                if (repo.disable === true || [0, -1].indexOf(repo.state) == -1) {
                    return;
                }
                repo.disable = true;
                API.repo.clone(repo);
            };
            $scope.repoUpdate = function (repo) {
                if (repo.disable === true || [2, -2].indexOf(repo.state) == -1) {
                    return;
                }
                repo.disable = true;
                API.repo.update(repo);
            };
            $scope.repoDelete = function (repo) {
                if (repo.disable === true || [-2, -1, 0, 2].indexOf(repo.state) == -1) {
                    return;
                }
                repo.disable = true;
                API.repo.delete(repo);
            };

            $scope.logJoin = function (log) {
                if(log) return log.replace('\n', '<br/>');
            };

            $scope.madalAdd = function () {
                $scope.error.url = false;

                var regExpStr = [
                    '^',
                    '(https?:\\\/\\\/)*',
                    '(?:([^:\\@]+)(?::([^\/@:]+))*@)*',
                    '(',
                    /**/'(?:[\\da-zа-я-\\.]+)+\\.[a-zа-я]{2,6}',
                    /**/'(?:\\\/[\\wа-я-\\.]+)*',
                    /**/'(?:\\\/([\\wа-я-\\.]+))\\.git',
                    ')\s*',
                    '$'
                ].join('');

                var re = new RegExp(regExpStr, 'i');

                if (!($scope.newRepoUrl && (data = $scope.newRepoUrl.match(re)))) {
                    $scope.error.url = true;
                    $alert({
                        error: {
                            code: -1,
                            message: 'Некорректный URL',
                            description: 'Введёный URL не является ссылкой на git репозиторий'
                        }
                    });
                    return;
                }

                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: 'modalTemplate.html',
                    controller: 'ModalAddCtrl',
                    size: 'md',
                    resolve: {
                        data: function () {
                            return data;
                        }
                    }
                });

                modalInstance.result.then(function () {
                    $scope.newRepoUrl = '';
                    reposGet();
                });

                return false;
            };

            $scope.modalEdit = function (repo) {
                if (repo.disable === true || [-2, -1, 0, 2].indexOf(repo.state) == -1) {
                    return;
                }
                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: 'modalTemplate.html',
                    controller: 'ModalEditCtrl',
                    size: 'md',
                    resolve: {
                        repo: function () {
                            return repo;
                        }
                    }
                });

                modalInstance.result.then(function () {
                    reposGet();
                });
            };
        }
    ]);