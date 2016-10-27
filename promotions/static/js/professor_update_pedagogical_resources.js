function personal_resourceController($scope) {
    $scope.links = [];
    $scope.files = [];

    $scope.addMore = function(kind, number) {
        if ($scope[kind].length > 0) {
            var new_number = $scope[kind][$scope[kind].length - 1] + 1;
        } else {
            var new_number = 0;
        }

        for (var i = 0; i < number; ++i) {
            $scope[kind].push(new_number + i);
        }
    }

    $scope.remove = function(kind, id) {
        $scope[kind].splice($scope[kind].indexOf(id), 1);
    }
}

function lesson_resourceController($scope) {
    $scope.links = [];
    $scope.files = [];

    $scope.addMore = function(kind, number) {
        if ($scope[kind].length > 0) {
            var new_number = $scope[kind][$scope[kind].length - 1] + 1;
        } else {
            var new_number = 0;
        }

        for (var i = 0; i < number; ++i) {
            $scope[kind].push(new_number + i);
        }
    }

    $scope.remove = function(kind, id) {
        $scope[kind].splice($scope[kind].indexOf(id), 1);
    }
}

function exercice_resourceController($scope) {
    $scope.links = [];
    $scope.files = [];

    $scope.addMore = function(kind, number) {
        if ($scope[kind].length > 0) {
            var new_number = $scope[kind][$scope[kind].length - 1] + 1;
        } else {
            var new_number = 0;
        }

        for (var i = 0; i < number; ++i) {
            $scope[kind].push(new_number + i);
        }
    }

    $scope.remove = function(kind, id) {
        $scope[kind].splice($scope[kind].indexOf(id), 1);
    }
}

function other_resourceController($scope) {
    $scope.links = [];
    $scope.files = [];

    $scope.addMore = function(kind, number) {
        if ($scope[kind].length > 0) {
            var new_number = $scope[kind][$scope[kind].length - 1] + 1;
        } else {
            var new_number = 0;
        }

        for (var i = 0; i < number; ++i) {
            $scope[kind].push(new_number + i);
        }
    }

    $scope.remove = function(kind, id) {
        $scope[kind].splice($scope[kind].indexOf(id), 1);
    }
}
