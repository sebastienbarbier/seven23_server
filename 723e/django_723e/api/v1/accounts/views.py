# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def api_login(request):
    results = {}
    
    form = AuthenticationForm(request.POST)
    
    # Check
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            results['code'] = 200
        else:
            # Return a 'disabled account' error message
            results['code'] = 201
            results['form'] = form.as_table()
    else:
        # Return an 'invalid login' error message.
        results['code'] = 202
        results['form'] = form.as_table()
    
    

    # On retourne le JSON du fichier
    j = simplejson.dumps(results, separators=(',',':'))
    return HttpResponse(j, mimetype='application/json')