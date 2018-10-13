from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template("home/home.html")
    # context = {"form": paste_form}
    return HttpResponse(template.render({}, request))