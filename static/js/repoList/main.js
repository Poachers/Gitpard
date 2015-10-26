gitpard = angular.module('gitpard');

gitpard
    .controller('repoList', ['$scope', '$http', '$uibModal', '$API', '$interval', function ($scope, $http, $modal, API, $interval) {

        $interval(function () {
            API.reposGet(function successCallback(data) {
                $scope.repos = data.results.reverse();
            });
        }, 1e3);

        $scope.repoClone = function (repo) {
            API.repoClone(repo.id, function (data) {
                $scope.addAlert(data.status);
            });
        };

        $scope.repoUpdate = function (repo) {
            API.repoUpdate(repo.id, function (data) {
                $scope.addAlert(data.status);
            });
        };

        $scope.repoDelete = function (repo) {
            API.repoDelete(repo.id, function (data) {
                $scope.addAlert(data.status);
            });
        };


        /**
         * ========================================
         * ==============  Alerts  ================
         * ========================================
         */
        $scope.alerts = [];

        $scope.addAlert = function (obj) {
            while ($scope.alerts.length > 4) {
                $scope.alerts.shift()
            }

            $scope.alerts.push({
                type: (obj.code == 5 ? 'success' : null),
                'dismiss-on-timeout': 5e3,
                msg: obj.message
            });
        };

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };


        /**
         * ========================================
         * =============  New repo  ===============
         * ========================================
         */
        $scope.openLoginModal = function () {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'myModalContent.html',
                controller: 'ModalAddCtrl',
                size: 'md',
                resolve: {
                    url: function () {
                        return $scope.newRepo;
                    }
                }
            });

            modalInstance.result.then(function (selectedItem) {
                $scope.newRepo = '';
                console.log('Modal sending at: ' + new Date(), selectedItem);
            }, function () {
                console.log('Modal dismissed at: ' + new Date());
            });
        };


        /**
         * ========================================
         * ============  Edit repo  ===============
         * ========================================
         */
        $scope.openEditModal = function (repo) {
            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'myModalContent.html',
                controller: 'ModalEditCtrl',
                size: 'md',
                resolve: {
                    id: function () {
                        return repo.id;
                    }
                }
            });

            modalInstance.result.then(function (selectedItem) {
                $scope.newRepo = '';
                console.log('Modal sending at: ' + new Date(), selectedItem);
            }, function () {
                console.log('Modal dismissed at: ' + new Date());
            });
        };
    }]);

gitpard
    .controller('ModalAddCtrl', ['$scope', '$modalInstance', 'url', '$API', function ($scope, $modalInstance, url, API) {

        $scope.lock = 0;
        $scope.inputModalNameError = false;
        $scope.inputModalLoginError = false;
        $scope.inputModalPasswordError = false;

        $scope.ok = function () {
            $scope.lock = false;
            $scope.inputModalNameError = false;
            $scope.inputModalLoginError = false;
            $scope.inputModalPasswordError = false;

            if (!$scope.name || $scope.name == '') {
                $scope.inputModalNameError = true;
            }

            if ($scope.lock == 'true') {
                if (!$scope.login || $scope.login == '') {
                    $scope.inputModalLoginError = true;
                }
                if (!$scope.password || $scope.password == '') {
                    $scope.inputModalPasswordError = true;
                }
            }

            if ($scope.inputModalNameError || $scope.inputModalLoginError || $scope.inputModalPasswordError) {
                return;
            }

            var request = {
                url: url,
                name: $scope.name,
                kind: +$scope.lock
            };

            if ($scope.lock == 1) {
                request.login = $scope.login;
                request.password = $scope.password
            }

            API.reposAdd(request, function successCallback(response) {
                console.log(response);
                $modalInstance.close(true);
            });
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);

//https://bitbucket.org/poachers/gitpard.git

gitpard
    .controller('ModalEditCtrl', ['$scope', '$modalInstance', 'id', '$API', function ($scope, $modalInstance, id, API) {
        API.repoGet(id, function (data) {
            $scope.name = data.name;
            $scope.lock = data.kind;
            $scope.login = data.login || '';
            $scope.password = '';
            $scope.url = data.url;
        });
        $scope.ok = function () {
            $scope.inputModalNameError = false;
            $scope.inputModalLoginError = false;
            $scope.inputModalPasswordError = false;

            if (!$scope.name || $scope.name == '') {
                $scope.inputModalNameError = true;
            }

            if ($scope.lock) {
                if (!$scope.login || $scope.login == '') {
                    $scope.inputModalLoginError = true;
                }
            }

            if ($scope.inputModalNameError || $scope.inputModalLoginError) {
                return;
            }

            var request = {
                id: id,
                url: $scope.url,
                name: $scope.name,
                kind: +$scope.lock
            };

            if ($scope.lock == 1) {
                request.login = $scope.login;
                request.password = $scope.password
            }

            API.repoSet(request, function successCallback(response) {
                console.log(response);
                $modalInstance.close(true);
            });
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);