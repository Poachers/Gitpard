gitpard = angular.module('gitpard');

gitpard
    .factory('$API', ['$http', '$alert', function ($http, $alert) {
        function defaultSuccessCallback(data) {
            console.log(data);
        }

        function callAPI(request, successCallback, errorCallback) {
            $http(request).then(function (response) {
                    if (response && response.data) {
                        (successCallback || defaultSuccessCallback)(response.data);
                    }
                }, function (a) {
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
                }, successCallback, errorCallback);
            },
            'repoTree': function (params, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch)
                }, successCallback, errorCallback);
            },
            'getFile': function (params, successCallback, errorCallback) {
                callAPI({
                    method: 'GET',
                    url: '/api/repositories/' + params.id + '/analysis/' + encodeURIComponent(params.branch) + params.file
                }, successCallback, errorCallback);
            },
            'reportsGet': function (params, successCallback, errorCallback) {
                successCallback(
                    {
                        "branches": [
                            "master",
                            'dev'
                        ],
                        "mask": {
                            "include": [
                                ".*py$",
                                ".*pyc$"
                            ],
                            "exclude": [
                                "__init__.py",
                                "__init__.pyc"
                            ]
                        },
                        "reports": [
                            {
                                "id": 1,
                                "repository": 44,
                                "branch": 'master',
                                "datetime": +(new Date),
                                "kind": 1,
                                "state": -1
                            },
                            {
                                "id": 2,
                                "repository": 44,
                                "branch": 'master',
                                "datetime": +(new Date),
                                "kind": 2,
                                "state": 0
                            },
                            {
                                "id": 3,
                                "repository": 44,
                                "branch": 'master',
                                "datetime": +(new Date),
                                "kind": 2,
                                "state": 1
                            }
                        ]

                    }
                );
            },
            'reportsTree': function (params, successCallback, errorCallback) {
                successCallback({
                    "project": [
                        {
                            "text": "Gitpard",
                            "type": "folder",
                            selectable: false,
                            "nodes": [
                                {
                                    "text": "__init__.py",
                                    "type": "file",
                                    "mask": false,
                                    color: "#ccc"
                                },
                                {
                                    "text": "manage.py",
                                    "type": "file",
                                    "color": "#000",
                                    "mask": true
                                }
                            ]
                        },
                        {
                            "text": "__init__.py",
                            "type": "file",
                            selectable: false,
                            "mask": false
                        },
                        {
                            "text": "manage.py",
                            "type": "file",
                            "mask": true
                        }
                    ]
                });
            }
        }
    }]);