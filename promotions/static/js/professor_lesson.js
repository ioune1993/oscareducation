function createTestController($scope, $http) {
    $scope.tests = [];
    $scope.skills = [];

    $scope.addNewTest = function() {
        $http.post("/professor/add_test_for_lesson/", {
            "name": $scope.name,
            "lesson": context.lessonId,
            "skills": $scope.toTestSkills,
        }).success(function(data, status, headers, config) {
            update_test_list();
            $scope.name = "";
        })
    }

    $scope.addSkillToTest = function() {
        $scope.toTestSkills.push($scope.currentlySelectedSkill);
        var toRemoveIndex;
        for (var index = 0; index < $scope.skills.length; index++) {
            if ($scope.skills[index].code == $scope.currentlySelectedSkill) {
                toRemoveIndex = index;
            }
        }
        $scope.skills.splice(toRemoveIndex, 1);
        $scope.currentlySelectedSkill = $scope.skills[0].code;
    }

    update_test_list = function () {
        $http.get("/professor/lesson_tests_and_skills/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.tests = data.tests;
                $scope.skills = data.skills;
                $scope.toTestSkills = [];
                $scope.currentlySelectedSkill = data.skills[0].code;
           })
    }

    update_test_list();
}
