function severalResourceController($scope) {
    $scope.students = [0, 1];

    $scope.addMoreStudent = function(number) {
        if ($scope.students.length > 0) {
            var new_number = $scope.students[$scope.students.length - 1] + 1;
            
        } else {
            var new_number = 0;
        }

        for (var i = 0; i < number; ++i) {
            $scope.students.push(new_number + i);
        }
    }

    $scope.removeStudent = function(id) {
        $scope.students.splice($scope.students.indexOf(id), 1);
    }
}
