from django.contrib import admin
from quiz.models import Problem, Quiz, Submission

# Register your models here.
admin.site.register(Problem)
admin.site.register(Quiz)
admin.site.register(Submission)