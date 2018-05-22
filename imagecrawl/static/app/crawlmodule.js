var app = angular.module('crawlApp', ["ngCookies","ngRoute","ngResource","ui.bootstrap","ui-notification"])

app.config(function($interpolateProvider,$resourceProvider) {
 $interpolateProvider.startSymbol('{[{');
 $interpolateProvider.endSymbol('}]}');
 $resourceProvider.defaults.stripTrailingSlashes = false;
});


app.run([
 '$http',
 '$cookies',
 function($http, $cookies) {
 $http.defaults.headers.post['X-CSRFToken'] =   $cookies.get('csrftoken');
 }
]);

app.run(['$rootScope','$http', function($rootScope,$http) {
  
}]);

app.directive('whenScrolled', function() {
    return function(scope, elm, attr) {
        var raw = elm[0];
        
        elm.bind('scroll', function() {
            if (raw.scrollTop + raw.offsetHeight >= raw.scrollHeight) {
                raw.scrollTop=raw.scrollTop-10;
                scope.$apply(attr.whenScrolled);
            }
        });
    };
});