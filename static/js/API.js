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
                    console.log(response);
                    $loading(false);
                    if (response && response.data) {
                        if (params && params.alert) {
                            $alert(response.data);
                        }
                        (successCallback || defaultSuccessCallback)(response.data);
                    }
                }, function (a) {
                    console.log(a);
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
                'get': function (params, successCallback, errorCallback, feature) {
                    var nPage = '?page=' + params.page;

                    callAPI({
                        metsod: 'GET',
                        url: '/api/repositories/' + nPage
                    }, successCallback, errorCallback);
                }
            },
            'repo': {
                'add': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/',
                        data: params
                    }, successCallback, errorCallback, {alert: 1});
                },
                'set': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/' + params.id + '/edit/',
                        data: params
                    }, successCallback, errorCallback, {alert: 1});
                },
                'clone': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.id + '/clone/'
                    }, successCallback, errorCallback, {alert: 1});
                },
                'update': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.id + '/update/'
                    }, successCallback, errorCallback, {alert: 1});
                },
                'delete': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/' + params.id + '/delete/'
                    }, successCallback, errorCallback, {alert: 1});
                }
            },
            'reports': {
                'get': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.id + '/report/'
                    }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
                },
                'tree': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'POST',
                        data: params,
                        url: '/api/repositories/' + params.id + '/report/tree'
                    }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
                },
                'create': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'POST',
                        data: params,
                        url: '/api/repositories/' + params.id + '/report/'
                    }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
                },
                'view': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'GET',
                        url: '/api/repositories/' + params.repo + '/report/' + params.id
                    }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
                },
                'delete': function (params, successCallback, errorCallback, feature) {
                    callAPI({
                        method: 'POST',
                        url: '/api/repositories/' + params.repository + '/report/' + params.id + '/delete/'
                    }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
                }
            },
            /* analysis */
            'repoBranches': function (id, successCallback, errorCallback, feature) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + id + '/analysis/'
                }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
            },
            'repoTree': function (params, successCallback, errorCallback, feature) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch)
                }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
            },
            'getFile': function (params, successCallback, errorCallback, feature) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch) + params.file
                }, successCallback, errorCallback, (feature || {alert: true, loading: true}));
            },
            'reportsGet': function (params, successCallback, errorCallback, feature) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/report/'
                }, successCallback, errorCallback, true);
            },
            'reportsTree': function (params, successCallback, errorCallback, feature) {
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