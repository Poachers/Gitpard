gitpard = angular.module('gitpard');

gitpard
    .factory('$API', ['$http', function ($http) {
        function defaultSuccessCallback(data) {
            console.log(data);
        }

        function callAPI(request, successCallback) {
            $http(request).then(function (response) {
                    if (response && response.data) {
                        (successCallback || defaultSuccessCallback)(response.data);
                    }
                }, function (a) {
                    if (/<[Hh][Tt][Mm][Ll]/.test(a.data)) {
                        var newWindow = window.open();
                        newWindow.document.write(a.data);
                    } else {
                        console.log('error', arguments);
                    }
                }
            );
        }

        return {
            'reposGet': function (successCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/'
                }, successCallback);
            },
            'reposAdd': function (params, successCallback) {
                if (!params)
                    throw new Error();
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/',
                    data: params
                }, successCallback);
            },
            'repoGet': function (id, successCallback) {
                callAPI({
                    methdod: 'GET',
                    url: '/api/repositories/' + id + '/edit/'
                }, successCallback);
            },
            'repoSet': function (params, successCallback) {
                if (!params)
                    throw new Error();
                callAPI({
                    methdod: 'POST',
                    url: '/api/repositories/' + params.id + '/edit/'
                }, successCallback);
            },
            'repoClone': function (id, successCallback) {
                callAPI({
                    methdod: 'GET',
                    url: '/api/repositories/' + id + '/clone/'
                }, successCallback);
            },
            'repoUpdate': function (id, successCallback) {
                callAPI({
                    methdod: 'GET',
                    url: '/api/repositories/' + id + '/update/'
                }, successCallback);
            },
            'repoDelete': function (id, successCallback) {
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + id + '/delete/'
                }, successCallback);
            }
        }
    }]);