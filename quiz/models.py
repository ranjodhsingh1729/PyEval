from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Create your models here.
Languages = {
    "1": "Assembly (NASM 2.14.02)",
    "2": "Bash (5.0.0)",
    "3": "Basic (FBC 1.07.1)",
    "4": "C (Clang 7.0.1)",
    "5": "C (GCC 7.4.0)",
    "6": "C (GCC 8.3.0)",
    "7": "C (GCC 9.2.0)",
    "8": "C# (Mono 6.6.0.161)",
    "9": "C++ (Clang 7.0.1)",
    "10": "C++ (GCC 7.4.0)",
    "11": "C++ (GCC 8.3.0)",
    "12": "C++ (GCC 9.2.0)",
    "13": "Clojure (1.10.1)",
    "14": "COBOL (GnuCOBOL 2.2)",
    "15": "Common Lisp (SBCL 2.0.0)",
    "16": "D (DMD 2.089.1)",
    "17": "Elixir (1.9.4)",
    "18": "Erlang (OTP 22.2)",
    "19": "Executable",
    "20": "F# (.NET Core SDK 3.1.202)",
    "21": "Fortran (GFortran 9.2.0)",
    "22": "Go (1.13.5)",
    "23": "Groovy (3.0.3)",
    "24": "Haskell (GHC 8.8.1)",
    "25": "Java (OpenJDK 13.0.1)",
    "26": "JavaScript (Node.js 12.14.0)",
    "27": "Kotlin (1.3.70)",
    "28": "Lua (5.3.5)",
    "29": "Objective-C (Clang 7.0.1)",
    "30": "OCaml (4.09.0)",
    "31": "Octave (5.1.0)",
    "32": "Pascal (FPC 3.0.4)",
    "33": "Perl (5.28.1)",
    "34": "PHP (7.4.1)",
    "35": "Plain Text",
    "36": "Prolog (GNU Prolog 1.4.5)",
    "37": "Python (2.7.17)",
    "38": "Python (3.8.1)",
    "39": "R (4.0.0)",
    "40": "Ruby (2.7.0)",
    "41": "Rust (1.40.0)",
    "42": "Scala (2.13.2)",
    "43": "SQL (SQLite 3.27.2)",
    "44": "Swift (5.2.3)",
    "45": "TypeScript (3.7.4)",
    "46": "Visual Basic.Net (vbnc 0.0.0.5943)",
}


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
    train_cases = models.JSONField()
    test_cases = models.JSONField()

    # Access
    authors = models.ManyToManyField(User, related_name="authored_problem_set")
    assigned = models.ManyToManyField(User, related_name="assigned_problem_set")


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
    source_lang = models.CharField(max_length=2, choices=Languages)
    time_usage = models.IntegerField(null=True)  # ms
    memory_usage = models.IntegerField(null=True)  # kb

    time_of_submission = models.DateTimeField(auto_now_add=True)

    verdict_choices = {
        "U": "Pending",
        "T": "Accepted",
        "F": "Rejected",
    }
    verdict = models.CharField(max_length=1, choices=verdict_choices, default="U")

    # Relation
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    # Access
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

