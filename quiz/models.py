from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Create your models here.
Languages = [
    {
        "id": 45,
        "name": "Assembly (NASM 2.14.02)"
    },
    {
        "id": 46,
        "name": "Bash (5.0.0)"
    },
    {
        "id": 47,
        "name": "Basic (FBC 1.07.1)"
    },
    {
        "id": 75,
        "name": "C (Clang 7.0.1)"
    },
    {
        "id": 76,
        "name": "C++ (Clang 7.0.1)"
    },
    {
        "id": 48,
        "name": "C (GCC 7.4.0)"
    },
    {
        "id": 52,
        "name": "C++ (GCC 7.4.0)"
    },
    {
        "id": 49,
        "name": "C (GCC 8.3.0)"
    },
    {
        "id": 53,
        "name": "C++ (GCC 8.3.0)"
    },
    {
        "id": 50,
        "name": "C (GCC 9.2.0)"
    },
    {
        "id": 54,
        "name": "C++ (GCC 9.2.0)"
    },
    {
        "id": 86,
        "name": "Clojure (1.10.1)"
    },
    {
        "id": 51,
        "name": "C# (Mono 6.6.0.161)"
    },
    {
        "id": 77,
        "name": "COBOL (GnuCOBOL 2.2)"
    },
    {
        "id": 55,
        "name": "Common Lisp (SBCL 2.0.0)"
    },
    {
        "id": 56,
        "name": "D (DMD 2.089.1)"
    },
    {
        "id": 57,
        "name": "Elixir (1.9.4)"
    },
    {
        "id": 58,
        "name": "Erlang (OTP 22.2)"
    },
    {
        "id": 44,
        "name": "Executable"
    },
    {
        "id": 87,
        "name": "F# (.NET Core SDK 3.1.202)"
    },
    {
        "id": 59,
        "name": "Fortran (GFortran 9.2.0)"
    },
    {
        "id": 60,
        "name": "Go (1.13.5)"
    },
    {
        "id": 88,
        "name": "Groovy (3.0.3)"
    },
    {
        "id": 61,
        "name": "Haskell (GHC 8.8.1)"
    },
    {
        "id": 62,
        "name": "Java (OpenJDK 13.0.1)"
    },
    {
        "id": 63,
        "name": "JavaScript (Node.js 12.14.0)"
    },
    {
        "id": 78,
        "name": "Kotlin (1.3.70)"
    },
    {
        "id": 64,
        "name": "Lua (5.3.5)"
    },
    {
        "id": 89,
        "name": "Multi-file program"
    },
    {
        "id": 79,
        "name": "Objective-C (Clang 7.0.1)"
    },
    {
        "id": 65,
        "name": "OCaml (4.09.0)"
    },
    {
        "id": 66,
        "name": "Octave (5.1.0)"
    },
    {
        "id": 67,
        "name": "Pascal (FPC 3.0.4)"
    },
    {
        "id": 85,
        "name": "Perl (5.28.1)"
    },
    {
        "id": 68,
        "name": "PHP (7.4.1)"
    },
    {
        "id": 43,
        "name": "Plain Text"
    },
    {
        "id": 69,
        "name": "Prolog (GNU Prolog 1.4.5)"
    },
    {
        "id": 70,
        "name": "Python (2.7.17)"
    },
    {
        "id": 71,
        "name": "Python (3.8.1)"
    },
    {
        "id": 80,
        "name": "R (4.0.0)"
    },
    {
        "id": 72,
        "name": "Ruby (2.7.0)"
    },
    {
        "id": 73,
        "name": "Rust (1.40.0)"
    },
    {
        "id": 81,
        "name": "Scala (2.13.2)"
    },
    {
        "id": 82,
        "name": "SQL (SQLite 3.27.2)"
    },
    {
        "id": 83,
        "name": "Swift (5.2.3)"
    },
    {
        "id": 74,
        "name": "TypeScript (3.7.4)"
    },
    {
        "id": 84,
        "name": "Visual Basic.Net (vbnc 0.0.0.5943)"
    }
]


class Problem(models.Model):
    # Info
    title = models.CharField(max_length=255)
    statement = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    note = models.TextField()

    # Constraints
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    input_stream = models.CharField(max_length=255)
    output_stream = models.CharField(max_length=255)

    # Cases
    cases = models.JSONField()

    # Ready
    complete = models.BooleanField()

    # Access
    authors = models.ManyToManyField(User, related_name="authored_problem_set")
    assigned = models.ManyToManyField(
        User, related_name="assigned_problem_set")


class Quiz(models.Model):
    # Info
    topic = models.CharField(max_length=255)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    instructions = models.TextField()

    # Relation
    problems = models.ManyToManyField(Problem)

    # Access
    authors = models.ManyToManyField(User, related_name="authored_quiz_set")
    assigned = models.ManyToManyField(User, related_name="assigned_quiz_set")


class Submission(models.Model):
    # Info
    source_code = models.TextField()
    source_lang = models.IntegerField()
    time_usage = models.IntegerField(null=True)  # ms
    memory_usage = models.IntegerField(null=True)  # kb

    time_of_submission = models.DateTimeField(auto_now_add=True)
    token = models.JSONField()

    verdict_choices = {
        "U": "Pending",
        "T": "Accepted",
        "F": "Rejected",
    }
    verdict = models.CharField(
        max_length=1, choices=verdict_choices, default="U")

    # Relation
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    # Access
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)


class Result(models.Model):
    # Info
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    data = models.JSONField()
