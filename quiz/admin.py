from django.contrib import admin
from quiz.models import Problem, Quiz, Submission, Result

# Register your models here.
admin.site.register(Problem)
admin.site.register(Quiz)
admin.site.register(Submission)
admin.site.register(Result)