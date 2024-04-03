from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path('problem/<int:id>', views.problem, name="problem"),
]