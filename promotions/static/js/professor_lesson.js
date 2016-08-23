function createTestController($scope, $http) {
    $scope.tests = [];
    $scope.skills1 = [];
    $scope.skills2 = [];  // for skills greater than level 4
    $scope.testType = "skills";

    $scope.addNewTest = function() {
        if ($scope.name === undefined || $scope.name.length == 0)
        {
            $("#alerts").html('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Vous devez donner un nom à votre test.</div>');
            return;
        }

        if ($scope.toTestSkills.length == 0) {
            $("#alerts").html('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Vous devez sélectionner des compétences pour votre test.</div>');
            return;
        }

        $http.post("/professor/add_test_for_lesson/", {
            "name": $scope.name,
            "lesson": context.lessonId,
            "skills": $scope.toTestSkills,
            "type": $scope.testType,
        }).success(function(data, status, headers, config) {
            update_test_list();
            $scope.name = "";
            // TODO: don't do that in javascript
            window.location.href = "..";
        })
    }

    $scope.addSkillToTest = function(skills_list_number) {
        $scope.toTestSkills.push($scope["currentlySelectedSkill" + skills_list_number]);
        var toRemoveIndex;
        for (var index = 0; index < $scope["skills" + skills_list_number].length; index++) {
            if ($scope["skills" + skills_list_number][index].code == $scope.currentlySelectedSkill) {
                toRemoveIndex = index;
            }
        }
        $scope["skills" + skills_list_number].splice(toRemoveIndex, 1);
        $scope["currentlySelectedSkill" + skills_list_number] = $scope["skills" + skills_list_number][0].code;
    }

    update_test_list = function () {
        $http.get("/professor/lesson_tests_and_skills/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.tests = data.tests;
                $scope.skills1 = data.skills1;
                $scope.skills2 = data.skills2;
                $scope.toTestSkills = [];
                $scope.currentlySelectedSkill1 = data.skills1[0].code;

                if (data.skills2.length > 0) {
                    $scope.currentlySelectedSkill2 = data.skills2[0].code;
                }
           })
    }

    update_test_list();
}
