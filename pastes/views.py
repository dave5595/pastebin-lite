from django.shortcuts import render
from django.views import View
from django.views.generic import *
from home.models import Paste

# Create your views here.
# TODO: Add delete function
class ShowPaste(View):
    template = "pastes/show_paste.html"

    def get_queryset(self):
        return Paste.objects.get(char_id=self.kwargs['char_id'])

    def get(self, request, char_id):
        print(char_id)
        paste = self.get_queryset()
        return render(request, self.template, {"paste": paste, "paste_text": paste.text})


