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
                console.log(data);
                $scope.addAlert(data.status);
            });
        };

        $scope.repoUpdate = function (repo) {
            API.repoUpdate(repo.id, function (data) {
                console.log(data);
                $scope.addAlert(data.status);
            });
        };

        $scope.repoDelete = function (repo) {
            API.repoDelete(repo.id, function (data) {
                console.log(data);
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
        $scope.inputNewRepoError = false;

        $scope.openLoginModal = function () {
            $scope.inputNewRepoError = false;
//https://bitbucket.org/poachers/gitpard.git

            var regExpStr = [
                '^',
                '(https?:\\\/\\\/)*',
                '(?:([^:\\@]+)(?::([^@:]+))*@)*',
                '(',
                /**/'(?:[\\da-zа-я-\\.]+)+\\.[a-zа-я]{2,6}',
                /**/'(?:\\\/[\\wа-я-\\.]+)*',
                /**/'(?:\\\/([\\wа-я-\\.]+))\\.git',
                ')',
                '$'
            ].join('');

            var re = new RegExp(regExpStr, 'i');

            if (!re.test($scope.newRepo)) {
                $scope.inputNewRepoError = true;
                return;
            }

            var data = $scope.newRepo.match(re);

            var modalInstance = $modal.open({
                animation: true,
                templateUrl: 'myModalContent.html',
                controller: 'ModalAddCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return data;
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
                    },
                    status: function () {
                        return repo.state;
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
         * ==========  Open analysis  =============
         * ========================================
         */
        $scope.openAnalysis = function(repo){
            console.log(repo);
            //location.href = '/api/repositories/' + repo.id + '/analysis/master/';
            location.href = '/analysis/#' + repo.id;
        };
    }]);

gitpard
    .controller('ModalAddCtrl', ['$scope', '$modalInstance', 'data', '$API', function ($scope, $modalInstance, data, API) {

        $scope.lock = {};


        $scope.lock.type = (data[2] && data[3] ? 1 : 0);

        $scope.inputModalNameError = false;
        $scope.inputModalLoginError = false;
        $scope.inputModalPasswordError = false;

        var url = (data[1] || 'https://') + data[4];
        $scope.name = data[5] || '';
        $scope.login = data[2] || '';
        $scope.password = data[3] || '';

        $scope.ok = function () {
            $scope.inputModalNameError = false;
            $scope.inputModalLoginError = false;
            $scope.inputModalPasswordError = false;

            if (!$scope.name || $scope.name == '') {
                $scope.inputModalNameError = true;
            }

            if ($scope.lock.type == 1) {
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
                kind: +$scope.lock.type
            };

            if ($scope.lock.type == 1) {
                request.login = $scope.login;
                request.password = $scope.password;
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

gitpard
    .controller('ModalEditCtrl', ['$scope', '$modalInstance', 'id', 'status', '$API', function ($scope, $modalInstance, id, status, API) {
        console.log(status);
        $scope.status = status;
        API.repoGet(id, function (data) {
            $scope.lock = {};
            $scope.name = data.name;
            $scope.lock.type = data.kind;
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

            if ($scope.lock.type) {
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
                kind: +$scope.lock.type
            };

            if ($scope.lock.type == 1) {
                request.login = $scope.login;
                request.password = $scope.password
            }

            API.repoSet(request, function successCallback(response) {
                $modalInstance.close(true);
            });
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);