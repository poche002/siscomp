var app = angular.module('usersApp', ['ui.grid']).
controller('users_controller', ['$scope', '$http', function($scope, $http) {
    
    $http.get("/users").
    success(function(data) {
      $scope.myData = data;
    })
    $scope.gridOptions = { 
      data: 'myData',
      columnDefs: [{
            field: 'user_id',
            displayName: 'ID'
        }, {
            field: 'fullname',
            displayName: 'Name'
        }, {
            field: 'email',
            displayName: 'e-Mail'
        }, {
            field: 'phone',
            displayName: 'Phone'
        }, { 
            name: 'Hyperlink',
            cellTemplate:'<div class="ngCellText" ng-class="col.colIndex()">' +
                   '<a href=/user.html?{{row.entity.email}}>Detail</a>' +
                   '</div>' }
        ]
    };
}]);