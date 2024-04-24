import json
from requests import Session
from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from .models import Problem, Quiz, Submission, Results, Languages

session = Session()
judge = "http://10.10.199.213:2358/submissions/?base64_encoded=false&wait=false"

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

            params = {
                "language_id": int(form["lang"]),
                "source_code": form["source_code"],
                "stdin": problem.cases["test"][0]["input"],
                "expected_output": problem.cases["test"][0]["output"]
            }
            token = session.post(judge, params=params)
            if token.ok:
                token = json.loads(token.text)
            else:
                return HttpResponse(f"{token.status_code}")

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
            return redirect(f'/resources/quiz/{id}')
    else:
        return redirect('/accounts/login?next=/resources/quiz/{id}/new_submission')


def results(request, id):
    if request.user.is_authenticated and request.user.authored_quiz_set.filter(id=id).exists():
        quiz = Quiz.objects.get(id=id)
        if Results.objects.filter(quiz=quiz).exists():
            result = Results.objects.gete(quiz=quiz)
            context = {"request": request, "quiz": quiz,
                       "result": result, "title": "Results"}
            return render(request, 'results.html', context=context)
        else:
            context = {"title": "Please Wait",
                       "msg": "Result Are Being Calculated!!!"}
            return render(request, 'msg.html', context=context)
    else:
        return redirect(f'/accounts/login?next=/resources/quiz/{id}/results')
