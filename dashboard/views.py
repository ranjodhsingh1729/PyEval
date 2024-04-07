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

                train_cases = form["train_cases"],
                test_cases = form["test_cases"],
            )
            new_problem.authors.add(request.user)
            new_problem.save()
            return redirect('/dashboard/your_problems')
    else:
        return redirect('/accounts/login?next=/dashboard/new_problem')

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
            return redirect('/dashboard/your_quizes')
    else:
        return redirect('/accounts/login?next=/dashboard/new_quiz')

def your_quizes(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Teachers").exists():
        quizes = request.user.authored_quiz_set.all()
        context = {"request": request, "quizes": quizes, "title": "Your Quizes"}
        return render(request, 'your_quizes.html', context=context)
    else:
        return redirect('/accounts/login?next=/dashboard/your_quizes')
