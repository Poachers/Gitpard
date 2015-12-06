gitpard = angular.module('gitpard', ['ui.bootstrap']);

gitpard
    .config(function ($interpolateProvider) {
        $interpolateProvider
            .startSymbol('{$')
            .endSymbol('$}');
    });

gitpard
    .config(['$httpProvider', function (provider) {
        var csrfToken = getCookie('csrftoken');
        provider.defaults.headers.common['X-CSRFToken'] = csrfToken;
        provider.defaults.headers.post['X-CSRFToken'] = csrfToken;

        provider.defaults.headers.post["Content-Type"] = 'application/json';

        provider.defaults.xsrfCookieName = 'csrftoken';
        provider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

gitpard = angular.module('gitpard');

gitpard
    .factory('$alert', ['$rootScope', function (rootScope) {
        rootScope.alerts = [];

        rootScope.closeAlert = function (index) {
            rootScope.alerts.splice(index, 1);
        };

        return function (obj) {
            while (rootScope.alerts.length > 1) {
                rootScope.alerts.shift()
            }
            if (obj.error) {
                var arr = [];
                if (typeof obj.error.length != 'number') {
                    arr.push(obj.error);
                } else {
                    arr = obj.error;
                }

                for (c = 0, j = arr.length; c < j; c++) {
                    rootScope.alerts.push({
                        type: 'danger',
                        'dismiss-on-timeout': 5e3,
                        msg: arr[c].description
                    });
                    console.log(arr[c])
                }
            } else if (obj.response) {
                rootScope.alerts.push({
                    type: 'success',
                    'dismiss-on-timeout': 5e3,
                    msg: obj.response.message
                });
            } else {
                console.warn(obj);
            }
        };
    }]);