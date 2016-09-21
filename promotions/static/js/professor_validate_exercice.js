function validateExerciceController($scope, $http, $sce, $timeout) {
    $scope.skillCode = "";
    $scope.html = "";
    $scope.yaml = "";
    $scope.yamlRendering = "";
    $scope.htmlRendering = "";
    $scope.image = null;
    $scope.base64img = "";

    $scope.questions = [{
        "instructions": "",
        "type": "",
        "answers": [{
            "text": "",
            "correct": false,
        }],
    }]

    $scope.yamlValidationResult = "";
    $scope.exerciceIsValid = false;

    $scope.uploadFile = function(files) {
        var reader = new FileReader();
        reader.readAsDataURL(files[0]);
        reader.addEventListener("load", function() {
            console.log("yay")
            $scope.base64img = reader.result;
            $scope.$digest();
        })
    }

    $scope.validateExercice = function() {
        var content = $scope.yaml;
        $http.post("validate/", {"questions": $scope.questions})
            .error(function() {
                console.log("error")
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger">Une erreur s\'est produite, nous en avons été alerté.</div>');
            })
            .success(function(data) {
                console.log("success");
                if (data.yaml.result == "error") {
                    // $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger"> <b>Erreur:</b> ' + data.yaml.message + '</b></div>');
                    $scope.exerciceIsValid = false;
                } else {
                    $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-success">' + data.yaml.message + '</b></div>');

                    $scope.yamlRendering = $sce.trustAsHtml(data.rendering);
                    $scope.htmlRendering = $sce.trustAsHtml($scope.html);

                    $timeout(function() {
                        $('#exercice-rendering-yaml input[type="submit"]').addClass("disabled");
                    }, 0);

                    $scope.exerciceIsValid = true;
                }
            })

    }

    $scope.proposeToOscar = function() {
        var yaml = $scope.yaml;
        var html = $scope.html;
        var skill_code = $scope.skillCode;

        if (!skill_code) {
            $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger"><b>Erreur :</b> vous devez sélectionner une compétence pour pouvoir proposer l\'exercice à Oscar.</div>');
            return;
        }

        $("#submit-pull-request").addClass("disabled");

        $http.post("pull-request/", {"questions": $scope.questions, "html": html, "skill_code": skill_code, "image": $scope.base64img})
            .success(function(data) {
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-success">L\'exercice a correctement été soumis, cette demande est visible ici: <a target="_blank" href="' + data + '">' + data + '</a></b></div>');

                $scope.yaml = "";
                $scope.html = "";
                $scope.skillCode = "";
                $scope.image = null;

                $scope.questions = [{
                    "instructions": "",
                    "type": "",
                    "answers": [{
                        "text": "",
                        "correct": false,
                    }],
                }]
            })
            .error(function() {
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger">Une erreur s\'est produite, nous en avons été alerté.</div>');
            })
            .always(function() {
                $timeout(function() {
                    $("#submit-pull-request").removeClass("disabled");
                }, 0);
            })
    }

    $scope.addAnswer = function(question) {
        question["answers"].push({
            "text": "",
            "correct": false,
        })
    }

    $scope.removeAnswer = function(question, answer) {
        question["answers"].splice(question["answers"].indexOf(answer), 1);
    }

    $scope.addQuestion = function() {
        $scope.questions.push({
            "instructions": "",
            "type": "",
            "answers": [{
                "text": "",
                "correct": false,
            }],
        })
    }

    $scope.removeQuestion = function(question) {
        $scope.questions.splice($scope.questions.indexOf(question), 1);
    }

}
