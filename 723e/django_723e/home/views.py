from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def homepage(request):
    form = AuthenticationForm()
    return render(request, 'home.html',  {
            'form': form,
        })