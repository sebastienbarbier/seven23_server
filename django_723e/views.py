"""
    Main views
"""
from django.http import HttpResponse
from django.template import loader

def home(request):
    """
        Home page when trying to open server URL.
        Should confirm everything is ok, and provide a link to a client.
    """
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
