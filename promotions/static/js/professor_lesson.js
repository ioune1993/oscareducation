function createTestController($scope, $http) {
    $scope.tests = [];

    $scope.addNewTest = function() {
        $http.post("/professor/add_test_for_lesson/", {
            "name": $scope.name,
            "lesson": context.lessonId,
            "skills": [],
        })
    }

    $http.get("/professor/lesson_tests/" + context.lessonId + ".json").
        success(function(data, status, headers, config) {
            $scope.tests = data;
        })
}
