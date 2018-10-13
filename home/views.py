from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Paste
from .forms import SubmitPasteForm

# Create your views here.
def home(request):
    """ Display the index page with the form to submit a paste, as well as the most recent pastes"""
    paste_form = SubmitPasteForm(request.POST or None, request=request)

    if paste_form.is_valid():
        paste_data = paste_form.cleaned_data

        user = None
        if request.user.is_authenticated():
            user = request.user

        paste = Paste()

        char_id = paste.add_paste(title=paste_data["title"],
                                  user=user,
                                  text=paste_data["text"],
                                  expiration=paste_data["expiration"],
                                  visibility=paste_data["visibility"],
                                  format=paste_data["syntax_highlighting"],
                                  encrypted=paste_data["encrypted"])

        # Redirect to the newly created paste
        return redirect("show_paste", char_id=char_id)

    template = loader.get_template("home/home.html")
    # context = {"form": paste_form}
    return HttpResponse(template.render({}, request))