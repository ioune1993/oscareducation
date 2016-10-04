function severalStudentsController($scope) {
    $scope.students = [0, 1];

    $scope.addAnotherStudent = function() {
        var new_number = $scope.students[$scope.students.length - 1] + 1;

        $scope.students.push(new_number);
    }
}
