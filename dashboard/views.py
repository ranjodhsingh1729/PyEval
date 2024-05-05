import json

from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from quiz.models import Problem, Quiz, Submission

# Create your views here.
def index(request):
    return redirect('dashboard/')

def dashboard(request):
    if request.user.is_authenticated:
        context = {"request": request, "title": "Dashboard"}
        return render(request, 'dashboard.html', context=context)
    else:
        return redirect('/accounts/login?next=/dashboard/')

def new_problem(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {"title": "Create Problem", "request": request}
            return render(request, 'new_problem.html', context=context)
        
        if request.method == "POST":
            form = request.POST
            new_problem = Problem.objects.create(
                time_limit = form["time_limit"],
                memory_limit = form["memory_limit"],
                input_stream = form["input_stream"],
                output_stream = form["output_stream"],

                title = form["title"],
                statement = form["statement"],
                input_format = form["input_format"],
                output_format = form["output_format"],
                note = form["note"],

                complete = False,

                cases = {
                    "test": [],
                    "train": [],
                }
            )
            new_problem.authors.add(request.user)
            new_problem.save()
            return redirect(f'/dashboard/new_problem/{new_problem.id}/add_cases')
    else:
        return redirect('/accounts/login?next=/dashboard/new_problem')
    
def add_cases(request, id):
    if request.user.is_authenticated:
        problem = Problem.objects.get(id=id)
        if request.method == "GET":
            context = {"title": "Create Problem", "request": request, "problem": problem, "train_cases": problem.cases.get("train"), "test_cases": problem.cases.get("test")}
            return render(request, 'add_cases.html', context=context)
        
        if request.method == "POST":
            form = request.POST
            if (form["action"] == "add"):
                case = {
                    "input": form["input"],
                    "output": form["output"]
                }
                problem.cases.get(form["case"]).append(case)
            elif (form["action"] == "delete"):
                problem.cases.get(form["item_type"]).pop(int(form["item_index"]) - 1)
            elif (form["action"] == "view"):
                case = problem.cases.get(form["item_type"])[int(form["item_index"]) - 1]
                return HttpResponse(
                    "<pre>" + json.dumps(case, indent=4) + "</pre>"
                )

            problem.save()
            return redirect(f'/dashboard/new_problem/{id}/add_cases')
    else:
        return redirect(f'/accounts/login?next=/dashboard/new_problem/{id}/add_cases')

def your_problems(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Teachers").exists():
        problems = request.user.authored_problem_set.all()
        context = {"request": request, "problems": problems, "title": "Your Problems"}
        return render(request, 'your_problems.html', context=context)
    else:
        return redirect('/accounts/login?next=/dashboard/your_problems')

def new_quiz(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {"title": "Create Quiz", "request": request}
            return render(request, 'new_quiz.html', context=context)
        
        if request.method == "POST":
            form = request.POST
            start = datetime.fromisoformat(
                form["start_date"]+"T"+form["start_time"]
            )
            stop = datetime.fromisoformat(
                form["stop_date"]+"T"+form["stop_time"]
            )
            new_quiz = Quiz.objects.create(
                topic = form["topic"],
                start = start,
                stop = stop,
                instructions = form["instructions"],
            )
            new_quiz.authors.add(request.user)
            new_quiz.save()
            return redirect(f'/dashboard/new_quiz/{new_quiz.id}/add_problems')
    else:
        return redirect('/accounts/login?next=/dashboard/new_quiz')

def add_problems(request, id):
    if request.user.is_authenticated:
        quiz = Quiz.objects.get(id=id)
        qprobs = quiz.problems.all()
        problems = Problem.objects.all()
        if request.method == "GET":
            context = {"title": "Create Quiz", "request": request, "qprobs": qprobs, "problems": problems}
            return render(request, 'add_problem.html', context=context)
        if request.method == "POST":
            form = request.POST
            problem = Problem.objects.get(id=int(form["prob"]))
            quiz.problems.add(problem)
            quiz.save()
            return redirect(f'/dashboard/new_quiz/{id}/add_problems')
    else:
        return redirect(f'/accounts/login?next=/dashboard/new_quiz/{id}/add_problems')


def your_quizes(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Teachers").exists():
        quizes = request.user.authored_quiz_set.all()
        context = {"request": request, "quizes": quizes, "title": "Your Quizes"}
        return render(request, 'your_quizes.html', context=context)
    else:
        return redirect('/accounts/login?next=/dashboard/your_quizes')