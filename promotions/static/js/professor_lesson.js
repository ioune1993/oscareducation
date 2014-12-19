function createTestController($scope, $http) {
    $scope.tests = [];
    $scope.skills = [];

    $scope.addNewTest = function() {
        $http.post("/professor/add_test_for_lesson/", {
            "name": $scope.name,
            "lesson": context.lessonId,
            "skills": [],
        }).success(function(data, status, headers, config) {
            update_test_list();
            $scope.name = "";
        })
    }

    update_test_list = function () {
        $http.get("/professor/lesson_tests_and_skills/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.tests = data.tests;
                $scope.skills = data.skills;
           })
    }

    update_test_list();
}
