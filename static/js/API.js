gitpard = angular.module('gitpard');

gitpard
    .factory('$API', ['$http', '$alert', function ($http, $alert) {
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
                        $alert(a.data);
                    }
                }
            );
        }

        return {
            'reposGet': function (page, successCallback) {

                if (typeof page == "function") {
                    successCallback = page;
                    page = 1;
                }

                npage = '?page=' + page;

                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + npage
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
                    method: 'GET',
                    url: '/api/repositories/' + id + '/edit/'
                }, successCallback);
            },
            'repoSet': function (params, successCallback) {
                if (!params)
                    throw new Error();
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + params.id + '/edit/',
                    data: params
                }, successCallback);
            },
            'repoClone': function (id, successCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/clone/'
                }, successCallback);
            },
            'repoUpdate': function (id, successCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/update/'
                }, successCallback);
            },
            'repoDelete': function (id, successCallback) {
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + id + '/delete/'
                }, successCallback);
            },

            /* analysis */
            'repoBranches': function (id, successCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/analysis/'
                }, successCallback);
            },
            'repoTree': function (params, successCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch)
                }, successCallback);
            },
            'getFile': function (params, successCallback) {
                console.log(params)
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch) + params.file
                }, successCallback);
            }
        }
    }]);