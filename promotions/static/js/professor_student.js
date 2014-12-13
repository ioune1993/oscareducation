function regeneratePasswordController($scope, $http) {
    $scope.askForNewPassword = function() {
        $http.post("/professor/regenerate_student_password/", {student_id: $scope.studentId}).
            success(function(data, status, headers, config) {
                $scope.password = data;
            })
    }
}
