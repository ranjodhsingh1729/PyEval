from django.db import models

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=255)

    # Constraints
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    input_source = models.CharField(max_length=255)
    output_source = models.CharField(max_length=255)

    # Info
    statement = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    
    train_cases = models.JSONField()
    test_cases = models.JSONField()

    note = models.TextField()


class Quiz(models.Model):
    # info
    

    # problems
    problems = models.ManyToManyField(Problem)