gitpard = angular.module('gitpard');

gitpard
    .factory('$API', ['$http', '$alert', '$loading', function ($http, $alert, $loading) {
        function defaultSuccessCallback(data) {
            console.log(data);
        }

        function callAPI(request, successCallback, errorCallback, params) {
            if (params && params.loading) {
                $loading();
            }
            $http(request).then(function (response) {
                    $loading(false);
                    if (response && response.data) {
                        if (params && params.alert) {
                            $alert(response.data);
                        }
                        (successCallback || defaultSuccessCallback)(response.data);
                    }
                }, function (a) {
                    $loading(false);
                    if (/<[Hh][Tt][Mm][Ll]/.test(a.data)) {
                        var newWindow = window.open();
                        newWindow.document.write(a.data);
                    } else {
                        (errorCallback ? errorCallback : (function () {
                        }))($alert(a.data));
                    }
                }
            );
        }

        return {
            'repos': {
                'get': function (params, successCallback, errorCallback) {
                    var nPage = '?page=' + params.page;

                    callAPI({
                        metsod: 'GET',
                        url: '/api/repositories/' + nPage
                    }, successCallback, errorCallback);
                }
            },
            'repo': {
                'add': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/',
                        data: params
                    }, successCallback, errorCallback, {alert: 1});
                },
                'set': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/' + params.id + '/edit/',
                        data: params
                    }, successCallback, errorCallback, {alert: 1});
                },
                'clone': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.id + '/clone/'
                    }, successCallback, errorCallback, {alert: 1});
                },
                'update': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.id + '/update/'
                    }, successCallback, errorCallback, {alert: 1});
                },
                'delete': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/' + params.id + '/delete/'
                    }, successCallback, errorCallback, {alert: 1});
                }
            },
            'reports': {
                'get': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.id + '/report/'
                    }, successCallback, errorCallback, {alert: true, loading: true});
                },
                'tree': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'POST',
                        data: params,
                        url: '/api/repositories/' + params.id + '/report/tree'
                    }, successCallback, errorCallback, {alert: true, loading: true});
                },
                'create': function (params, successCallback, errorCallback) {
                    callAPI({
                        method: 'POST',
                        data: params,
                        url: '/api/repositories/' + params.id + '/report/'
                    }, successCallback, errorCallback, {alert: true, loading: true});
                }
            },
            /* analysis */
            'repoBranches': function (id, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/analysis/'
                }, successCallback, errorCallback);
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
                //console.log(JSON.stringify(params));
                callAPI({
                    method: 'POST',
                    url: '/api/repositories/' + id + '/report/tree',
                    data: params
                }, successCallback, errorCallback, true);
            }
        }
    }]);