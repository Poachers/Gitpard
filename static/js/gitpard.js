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

gitpard
    .factory('$loading', ['$rootScope', function (rootScope) {
        return function (on) {
            if (on === false) {
                rootScope.mainLoading = true;
            } else {
                rootScope.mainLoading = false;
            }
        };
    }]);

gitpard
    .factory('$alert', ['$rootScope', function (rootScope) {
        rootScope.alerts = [];

        rootScope.closeAlert = function (index) {
            rootScope.alerts.splice(index, 1);
        };

        function rec(obj){
            for (var item in obj){
                if(typeof obj[item] == 'object'){
                    if(obj[item].status || obj[item].message){
                        rootScope.alerts.push(obj[item]);
                    } else{
                        rec(obj[item]);
                    }
                }
            }
        }

        return function (obj) {
            while (rootScope.alerts.length > 2) {
                rootScope.closeAlert(0);
            }

            rec(obj);

            return obj;
        };
    }])
;

gitpard
    .service('$easterEgg', ['$rootScope', function (rootScope) {
        rootScope.__defineGetter__('toggleEasterEgg', function () {
            rootScope.easterEgg = !rootScope.easterEgg;
        });
    }]);