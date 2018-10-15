from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic import CreateView, DetailView
from django.template import loader
from .models import Paste
from django.core import serializers
from .forms import SubmitPasteForm
from django.views import View

class HomeView(View):
    form_class = SubmitPasteForm
    template = "home/home.html"

    def get(self, request):
        form = self.form_class(request=request)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None,request=request)
        if form.is_valid():
            print("valid form")
            paste_data = form.cleaned_data
            paste = Paste()
            # char_id = paste.add_paste(title=paste_data["title"],
            #                                   text=paste_data["text"],
            #                                   expiration=paste_data["expiration"],)

            saved_paste = paste.add_paste(title=paste_data["title"],
                                              text=paste_data["text"],
                                              expiration=paste_data["expiration"],)
            # Redirect to the newly created paste
            return redirect("show_paste", char_id=saved_paste.char_id)

        return render(request, self.template, {'form': form})





# # Create your views here.
# def home(request):
#     """ Display the index page with the form to submit a paste, as well as the most recent pastes"""
#     paste_form = SubmitPasteForm(request.POST or None, request=request)
#     print("paste form",paste_form)
#     print(paste_form.is_valid())
#     if paste_form.is_valid():
#         paste_data = paste_form.cleaned_data
#         paste = Paste()
#
#         # char_id = paste.add_paste(title=paste_data["title"],
#         #                           text=paste_data["text"],
#         #                           expiration=paste_data["expiration"],)
#         saved_paste = paste.add_paste(title=paste_data["title"],
#                                   text=paste_data["text"],
#                                   expiration=paste_data["expiration"],)
#
#         print("paste obj id", saved_paste.char_id)
#         # Redirect to the newly created paste
#         # return redirect("show_paste", char_id=char_id)
#         data = serializers.serialize('json', saved_paste)
#         return HttpResponse(data, content_type='application/json')
#
#     template = loader.get_template("home/home.html")
#     # context = {"form": paste_form}
#     return HttpResponse(template.render({}, request))