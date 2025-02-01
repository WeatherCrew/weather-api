from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Weather API</h1><p>Use /docs for the api documentation.</p>")
