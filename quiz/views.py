import json
import threading
from requests import Session
from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import get_user_model

from .models import Problem, Quiz, Submission, Result, Languages


User = get_user_model()

session = Session()
judge = "http://10.10.215.167:2358/submissions/?base64_encoded=false&wait=false"


def status_uri(token):
    return f"http://10.10.215.167:2358/submissions/{token}?base64_encoded=false&fields=time,memory,status"

def get_status(submission):
    status = session.get(status_uri(submission.token))
    if status.ok:
        status = json.loads(status.text)
        submission.time_usage = status["time"]
        submission.memory_usage = status["memory"]
        if status["status"]["id"] == 3:
            submission.verdict = "T"
        elif status["status"]["id"] < 3:
            submission.vredict = "U"
        else:
            submission.verdict = "F"
    else:
        pass

def calculate_result(quiz):
    data = {}
    submissions = quiz.submission_set.all()
    for submission in submissions:
        if submission.author.id in data:
            data[submission.author.id][submission.verdict] = data[submission.author.id].get(submission.verdict, 0) + 1
        else:
            data[submission.author.id] = {submission.verdict: 1}

    result = Result.objects.create(
        quiz = quiz,
        data = data
    )
    result.save()


# Create your views here.
def problem(request, id):
    if request.user.is_authenticated and request.user.authored_problem_set.filter(id=id).exists():
        problem = Problem.objects.get(id=id)
        context = {"request": request, "problem": problem,
                   "title": problem.title, "examples": [1]}
        return render(request, 'problem.html', context=context)
    else:
        return redirect(f'/accounts/login?next=/resources/problem/{id}')


def quiz(request, id):
    if request.user.is_authenticated and request.user.authored_quiz_set.filter(id=id).exists():
        quiz = Quiz.objects.get(id=id)
        context = {"request": request, "quiz": quiz, "title": quiz.topic}
        return render(request, 'quiz.html', context=context)
    else:
        return redirect(f'/accounts/login?next=/resources/quiz/{id}')


def new_submission(request, id):
    if request.user.is_authenticated:
        quiz = Quiz.objects.get(id=id)
        problems = quiz.problems.all()
        if request.method == "GET":
            context = {"title": "Submit Your Code", "quiz": quiz,
                       "problems": problems, "languages": Languages, "request": request}
            return render(request, 'new_submission.html', context=context)

        if request.method == "POST":
            form = request.POST
            problem = Problem.objects.get(id=int(form["problem"]))

            token = {"submissions": []}
            for case in problem.cases["test"]:
                params = {
                    "language_id": int(form["lang"]),
                    "source_code": form["source_code"],
                    "stdin": case["input"],
                    "expected_output": case["output"]
                }

                res = session.post(judge, params=params)
                if res.ok:
                    token["submissions"].append(json.loads(res.text))
                else:
                    return HttpResponse(f"{res.status_code}")

            new_submission = Submission.objects.create(
                source_lang=form["lang"],
                source_code=form["source_code"],
                time_of_submission=datetime.now(),

                token=token,

                quiz=quiz,
                problem=problem,
                author=request.user,
            )
            new_submission.save()

            threading.Thread(target=get_status, args=(new_submission,)).start()

            return redirect(f'/resources/quiz/{id}')
    else:
        return redirect('/accounts/login?next=/resources/quiz/{id}/new_submission')


def results(request, id):
    if request.user.is_authenticated and request.user.authored_quiz_set.filter(id=id).exists():
        quiz = Quiz.objects.get(id=id)
        if Result.objects.filter(quiz=quiz).exists():
            result = Result.objects.get(quiz=quiz)
            students = {id: User.objects.get(id=id).username for id in result.data}
            context = {"request": request, "quiz": quiz,
                       "result": result.data, "title": "Results"}
            return render(request, 'result.html', context=context)
        else:
            threading.Thread(target=calculate_result, args=(quiz,)).start()

            context = {"title": "Please Wait",
                       "msg": "Result Are Being Calculated!!!"}
            return render(request, 'msg.html', context=context)
    else:
        return redirect(f'/accounts/login?next=/resources/quiz/{id}/results')
