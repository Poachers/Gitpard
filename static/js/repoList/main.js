$(document).ready(function () {
    $('#loading').css({display: 'none'});
});

gitpard = angular.module('gitpard');

gitpard
    .controller('repoList', ['$scope', '$http', '$uibModal', '$API', '$alert', '$interval', function ($scope, $http, $modal, API, $alert, $interval) {

        function getSearch(url) {
            var loc;

            if (!url) {
                loc = location;
            } else {
                loc = new URL(url);
            }

            var search = loc.search.replace('?', ''),
                params = search.split('&'),
                temp,
                result = {};

            for (var key in params) {
                temp = params[key].split('=');
                if (temp[1] || temp[1] === false) {
                    result[temp[0]] = temp[1];
                } else {
                    result[temp[0]] = true;
                }
            }
            return result;
        }

        $interval(function () {
            var page = getSearch()['page'];

            if (!page) {
                location.search = '?page=' + (page || 1);
            }

            API.reposGet(page, function successCallback(data) {
                $scope.repos = data.results.reverse();


                if (data.previous || data.next) {
                    $scope.noPages = 'show';
                    if (!data.previous) {
                        $scope.previousPage = {
                            href: '#page',
                            disabled: 'disabled'
                        };
                    } else {
                        $scope.previousPage = {
                            href: '/?page=' + (getSearch(data.previous)['page'] || 1),
                            disabled: ''
                        };
                    }
                    if (!data.next) {
                        $scope.nextPage = {
                            href: '#page',
                            disabled: 'disabled'
                        };
                    } else {
                        $scope.nextPage = {
                            href: '/?page=' + (getSearch(data.next)['page'] || 1),
                            disabled: ''
                        };
                    }
                }
            }, function(){
                    location.href = '/';
            });
        }, 1e3);

        $scope.previousPage = {};
        $scope.nextPage = {};

        $scope.repoClone = function (repo) {
            API.repoClone(repo.id, function (data) {
                $alert({response: data.status});
            });
        };

        $scope.repoUpdate = function (repo) {
            API.repoUpdate(repo.id, function (data) {
                $alert({response: data.status});
            });
        };

        $scope.repoDelete = function (repo) {
            API.repoDelete(repo.id, function (data) {
                $alert({response: data.status});
            });
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
                '(?:([^:\\@]+)(?::([^\/@:]+))*@)*',
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
                $alert({error: {description: 'Некорректный URL'}});
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
        $scope.openAnalysis = function (repo) {
            location.href = '/analysis/#' + repo.id;
        };
        $scope.openReports = function (repo) {
            location.href = '/report/#' + repo.id;
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

        $scope.url = url;

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
                if (response.error)
                    console.log(response.error);
                $modalInstance.close(true);
            });
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }]);

gitpard
    .controller('ModalEditCtrl', ['$scope', '$modalInstance', 'id', 'status', '$API', function ($scope, $modalInstance, id, status, API) {
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