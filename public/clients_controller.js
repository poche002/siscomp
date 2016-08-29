var clients_app = angular.module('clientsApp', ['ui.grid']).
controller('clients_controller', ['$scope', '$http', function($scope, $http) {
    
    
    $http.get("/clients").
    success(function(data) {
        $scope.myData = data;
    })
    
    $scope.gridOptions = { 
    data: 'myData',
    columnDefs: [{
            field: 'client_system_id',
            displayName: 'ID'
        }, {
            field: 'detail',
            displayName: 'Detail'
        }, {
            field: 'last_keepalive',
            displayName: 'Last keepalive'
        }, {
            field: 'state',
            displayName: 'State'
        }, { 
            name: 'Hyperlink',
            cellTemplate:'<div class="ngCellText" ng-class="col.colIndex()">' +
                   '<a href=http://localhost:8080/client_system.html?{{row.entity.client_system_id}}>Detail</a>' +
                   '</div>' }
        ]
    };
}]);