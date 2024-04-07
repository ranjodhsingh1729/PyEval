from django.urls import path
from . import views

urlpatterns = [
    path('problem/<int:id>', views.problem, name="problem"),
    path('quiz/<int:id>', views.quiz, name="quiz"),
    path('quiz/<int:id>/new_submission', views.new_submission, name="new_submission"),
]