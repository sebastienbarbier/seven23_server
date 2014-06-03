from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/home/')
def dashboard(request):
    return render(request, 'index_dashboard.html')

# Create your views here.
@login_required(login_url='/home/')
def liste(request):
	
    return render(request, 'dashboard.html')

# Create your views here.
@login_required(login_url='/home/')
def details(request):
    return render(request, 'details.html')