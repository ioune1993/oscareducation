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

    $scope.addSkillToTest = function() {
        console.log($scope.currentlySelectedSkill);
    }

    update_test_list = function () {
        $http.get("/professor/lesson_tests_and_skills/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.tests = data.tests;
                $scope.skills = data.skills;
                $scope.currentlySelectedSkill = data.skills[0].code;
           })
    }

    update_test_list();
}
