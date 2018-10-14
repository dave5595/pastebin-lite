from django.shortcuts import render
from django.views import View
from django.views.generic import *
from home.models import Paste

# Create your views here.

class ShowPaste(View):
    template = "pastes/show_paste.html"

    def get_queryset(self):
        return Paste.objects.get(char_id=self.kwargs['char_id'])

    def get(self, request, char_id):
        paste = self.get_queryset()
        print("paste", paste)
        return render(request, self.template, {"paste": paste, "paste_text": paste.text})


# def show_paste(request, char_id, raw=False, download=False, version=None):
#     return render(request, "pastes/show_paste.html", {"paste": paste,"paste_text": paste_text})
#