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