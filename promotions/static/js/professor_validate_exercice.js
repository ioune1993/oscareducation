function validateExerciceController($scope, $http, $sce, $timeout) {
    $scope.skillCode = "";
    $scope.html = "";
    $scope.yaml = "";
    $scope.yamlRendering = "";
    $scope.htmlRendering = "";

    $scope.yamlValidationResult = "";
    $scope.exerciceIsValid = false;

    $scope.validateExercice = function() {
        var content = $scope.yaml;
        $http.post("validate/", {"yaml": content})
            .error(function() {
                console.log("error")
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger">Une erreur s\'est produite, nous en avons été alerté.</div>');
            })
            .success(function(data) {
                console.log("success");
                if (data.yaml.result == "error") {
                    $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger"> <b>Erreur:</b> ' + data.yaml.message + '</b></div>');
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

        // TODO: complain if no yaml or no skill code

        $http.post("pull-request/", {"yaml": yaml, "html": html, "skill_code": skill_code})
            .success(function(data) {
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-success">L\'exercice a correctement été soumis, cette demande est visible ici: <a target="_blank" href="' + data + '">' + data + '</a></b></div>');

                $scope.yaml = "";
                $scope.html = "";
                $scope.skillCode = "";
            })
        .error(function() {
            $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger">Une erreur s\'est produite, nous en avons été alerté.</div>');
        })
        .always(function() {
            $("#submit-pull-request").removeClass("disabled");
        })
    }
}
