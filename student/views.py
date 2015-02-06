from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from examinations.models import TestStudent

from utils import user_is_student


@user_is_student
def dashboard(request):
    return render(request, "student/dashboard.haml", {})


@user_is_student
def pass_test(request, pk):
    test_student = get_object_or_404(TestStudent, pk=pk)

    if test_student.student != request.user.student:
        raise PermissionDenied()

    return render(request, "examinations/pass_test.haml", {
        "test": test_student.test,
    })
