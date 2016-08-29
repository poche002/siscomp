var app = angular.module('usersApp', ['ui.grid']).
controller('users_controller', ['$scope', '$http', function($scope, $http) {
    
    $http.get("/users").
    success(function(data) {
      $scope.myData = data;
    })
    //$scope.myData = [{name: "Moroni", age: 50, mail: "a"},
    //                 {name: "Tiancum", age: 43, mail: "a"},
    //                 {name: "Jacob", age: 27, mail: "a"},
    //                 {name: "Nephi", age: 29, mail: "a"},
    //                 {name: "Enos", age: 34, mail: "a"}];
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
            displayName: 'Phone' //"http://localhost:8080/users/?_method=get_one_by_email;email_param=
        }, { 
            name: 'Hyperlink',
            cellTemplate:'<div class="ngCellText" ng-class="col.colIndex()">' +
                   '<a href=http://localhost:8080/user.html?{{row.entity.email}}>Detail</a>' +
                   '</div>' }
        ]
    };
}]);