from django.shortcuts import render

from promotions.models import Lesson

from utils import user_is_student


@user_is_student
def dashboard(request):
    return render(request, "student/dashboard.haml", {
        "lessons": Lesson.objects.filter(students=request.user.student)
    })
