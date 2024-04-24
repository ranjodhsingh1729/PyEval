from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/new_problem', views.new_problem, name="new_problem"),
    path('dashboard/new_problem/<int:id>/add_cases', views.add_cases, name="add_cases"),
    path('dashboard/your_problems', views.your_problems, name="your_problems"),
    path('dashboard/new_quiz', views.new_quiz, name="new_quiz"),
    path('dashboard/new_quiz/<int:id>/add_problems', views.add_problems, name="add_problems"),
    path('dashboard/your_quizes', views.your_quizes, name="your_quizes"),
]
