var _cookies;
function _initCookies() {
    _cookies = {};
    var ca = document.cookie.split(';');
    var re = /^[\s]*([^\s]+?)$/i;
    for (var i = 0, l = ca.length; i < l; i++) {
        var c = ca[i].split('=');
        if (c.length == 2) {
            _cookies[c[0].match(re)[1]] = unescape(c[1].match(re) ? c[1].match(re)[1] : '');
        }
    }
}
function getCookie(name) {
    _initCookies();
    return _cookies[name];
}
function getCookie(name) {
    _initCookies();
    return _cookies[name];
}