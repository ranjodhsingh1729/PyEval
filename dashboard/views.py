from django.shortcuts import render, redirect
from django.http.response import HttpResponse

# Create your views here.
def index(request):
    return redirect('dashboard/')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', context={})
    else:
        return redirect('/accounts/login?next=/dashboard/')