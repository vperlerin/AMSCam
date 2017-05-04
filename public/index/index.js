angular.module('myApp', [
  'ngRoute',
  'home' 
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/home'});
}]);
