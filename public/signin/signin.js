'use strict';

angular.module('signin', ['base64','ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/signin', {
    templateUrl: '../signin/signin.html',
    controller: 'SignInCtrl'
  });
}])
  

.controller('SignInCtrl',['$scope','$http','$base64','$window','$location',function($scope,$http,$base64,$window,$location){

 
$scope.signIn = function(){
	var username = $scope.username;
	var password = $scope.password;

	
	var authdata = $base64.encode(username + ':' + password);

	
	$http.defaults.headers.common = {"Access-Control-Request-Headers": "accept, origin, authorization"};
    	$http.defaults.headers.common = {"Access-Control-Expose-Headers": "Origin, X-Requested-With, Content-Type, Accept"};
	$http.defaults.headers.common["Cache-Control"] = "no-cache";
    	$http.defaults.headers.common.Pragma = "no-cache";
    	$http.defaults.headers.common['Authorization'] = 'Basic '+authdata;
    
	$http({method: 'GET',cache: false, url: 'http://127.0.0.1:5000/user/'+ username}).
            success(function(data, status, headers, config) {
		
		
		console.log(data);
            }).
            error(function(data, status, headers, config) {
                console.log(data,status);
            });
       
};

	
}]);

