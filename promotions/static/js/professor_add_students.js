function severalStudentsController($scope) {
    $scope.students = [0, 1];

    $scope.addAnotherStudent = function() {
        if ($scope.students.length > 0) {
            var new_number = $scope.students[$scope.students.length - 1] + 1;
        } else {
            var new_number = 0;
        }

        $scope.students.push(new_number);
    }

    $scope.removeStudent = function(id) {
        $scope.students.splice($scope.students.indexOf(id), 1);
    }
}
