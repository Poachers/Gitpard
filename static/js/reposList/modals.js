gitpard.controller('ModalAddCtrl',
    ['$scope', '$modalInstance', 'data', '$API',
        function ($scope, $modalInstance, data, API) {
            $scope.kinds = [
                {name: 'Открытый репозитори', value: 0},
                {name: 'Приватный репозиторий', value: 1}
            ];

            $scope.error = {};

            $scope.repo = {
                url: (data[1] || 'https://') + data[4],
                login: data[2] || '',
                password: data[3] || '',
                name: data[5] || '',
                kind: $scope.kinds[(data[2] && data[3] ? 1 : 0)]
            };

            $scope.ok = function () {
                $scope.disabled = true;
                $scope.error.name = false;
                $scope.error.login = false;
                $scope.error.password = false;

                if (!$scope.repo.name || $scope.repo.name == '') {
                    $scope.error.name = true;
                }

                if ($scope.repo.kind.value) {
                    if (!$scope.repo.login || $scope.repo.login == '') {
                        $scope.error.login = true;
                    }
                    if (!$scope.repo.password || $scope.repo.password == '') {
                        $scope.error.password = true;
                    }
                }

                if ($scope.error.name || $scope.error.login || $scope.error.password) {
                    $scope.disabled = false;
                    return;
                }

                var request = angular.copy($scope.repo);
                request.kind = request.kind.value || 0;

                if (!request.kind) {
                    request.login = '';
                    request.password = '';
                }

                $scope.loading = true;

                API.repo.add(request, function successCallback(response) {
                    if (!response.error) {
                        $modalInstance.close(true);
                    }
                }, function errorCallback(error) {
                    $scope.loading = false;
                    $scope.disabled = false;
                });
            };

            $scope.cancel = function () {
                $modalInstance.dismiss(false);
            };
        }]);

gitpard.controller('ModalEditCtrl',
    ['$scope', '$modalInstance', 'repo', '$API',
        function ($scope, $modalInstance, repo, API) {
            $scope.kinds = [
                {name: 'Открытый репозитори', value: 0},
                {name: 'Приватный репозиторий', value: 1}
            ];

            $scope.error = {};

            $scope.repo = angular.copy(repo);
            $scope.repo.kind = $scope.kinds[$scope.repo.kind];

            $scope.ok = function () {
                $scope.disabled = true;
                $scope.error.name = false;
                $scope.error.login = false;
                $scope.error.password = false;

                if (!$scope.repo.name || $scope.repo.name == '') {
                    $scope.error.name = true;
                }

                if ($scope.repo.kind.value) {
                    if (!$scope.repo.login || $scope.repo.login == '') {
                        $scope.error.login = true;
                    }
                    if (!$scope.repo.password || $scope.repo.password == '') {
                        $scope.error.password = true;
                    }
                }

                if ($scope.error.name || $scope.error.login || $scope.error.password) {
                    $scope.disabled = false;
                    return;
                }

                var request = angular.copy($scope.repo);
                request.kind = request.kind.value || 0;

                if (!request.kind) {
                    request.login = '';
                    request.password = '';
                }

                $scope.loading = true;

                API.repo.set(request, function successCallback(response) {
                    console.log(arguments);
                    if (!response.error) {
                        $modalInstance.close(true);
                    }
                }, function errorCallback(error) {
                    console.log(arguments);
                    $scope.loading = false;
                    $scope.disabled = false;
                });
            };

            $scope.cancel = function () {
                $modalInstance.dismiss(false);
            };
        }]);