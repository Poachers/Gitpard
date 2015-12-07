gitpard = angular.module('gitpard');

gitpard
    .factory('$API', ['$http', '$alert', '$loading', function ($http, $alert, $loading) {
        function defaultSuccessCallback(data) {
            console.log(data);
        }

        function callAPI(request, successCallback, errorCallback, loading) {
            if (loading) {
                $loading();
            }
            $http(request).then(function (response) {
                    $loading(false);
                    if (response && response.data) {
                        (successCallback || defaultSuccessCallback)(response.data);
                    }
                }, function (a) {
                    $loading(false);
                    if (/<[Hh][Tt][Mm][Ll]/.test(a.data)) {
                        var newWindow = window.open();
                        newWindow.document.write(a.data);
                    } else {
                        (errorCallback?errorCallback:(function(){}))($alert(a.data));
                    }
                }
            );
        }

        return {
            'reposGet': function (page, successCallback, errorCallback) {

                if (typeof page == "function") {
                    successCallback = page;
                    page = 1;
                }

                npage = '?page=' + page;

                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + npage
                }, successCallback, errorCallback);
            },
            'reposAdd': function (params, successCallback, errorCallback) {
                if (!params)
                    throw new Error();
                if (!params.login)       params.login = '';
                if (!params.password)    params.password = '';
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/',
                    data: params
                }, successCallback, errorCallback);
            },
            'repoGet': function (id, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/edit/'
                }, successCallback, errorCallback);
            },
            'repoSet': function (params, successCallback, errorCallback) {
                if (!params)
                    throw new Error();
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + params.id + '/edit/',
                    data: params
                }, successCallback, errorCallback);
            },
            'repoClone': function (id, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/clone/'
                }, successCallback, errorCallback);
            },
            'repoUpdate': function (id, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/update/'
                }, successCallback, errorCallback);
            },
            'repoDelete': function (id, successCallback, errorCallback) {
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + id + '/delete/'
                }, successCallback, errorCallback);
            },

            /* analysis */
            'repoBranches': function (id, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/analysis/'
                }, successCallback, errorCallback, true);
            },
            'repoTree': function (params, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch)
                }, successCallback, errorCallback, true);
            },
            'getFile': function (params, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch) + params.file
                }, successCallback, errorCallback, true);
            },
            'reportsGet': function (params, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/report/'
                }, successCallback, errorCallback, true);
            },
            'reportsTree': function (params, successCallback, errorCallback) {
                var id = params.id;
                delete params.id;
                console.log(JSON.stringify(params));
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + id + '/report/tree',
                    data: params
                }, successCallback, errorCallback, true);
            }
        }
    }]);