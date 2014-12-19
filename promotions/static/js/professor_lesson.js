function createTestController($scope, $http) {
    $scope.tests = [];

    $scope.addNewTest = function() {
        
    }

    $http.get("/professor/lesson_tests/" + context.lessonId + ".json").
        success(function(data, status, headers, config) {
            $scope.tests = data;
        })
}
