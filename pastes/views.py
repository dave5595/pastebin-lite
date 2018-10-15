from django.shortcuts import render,redirect
from django.views import View

from django.views.generic import *
from home.models import Paste
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
# TODO: Add delete function
class ShowPaste(View):
    template = "pastes/show_paste.html"

    def get_queryset(self):
        return Paste.objects.get(char_id=self.kwargs['char_id'] )

    def get(self, request, char_id):
        print(char_id)
        paste = self.get_queryset()
        #save current Paste in session
        request.session['paste'] = paste
        return render(request, self.template, {"paste": paste, "paste_text": paste.text})

class ConfirmDelete(View):
   template = "pastes/confirm_delete_paste.html"

   def get(self, request, char_id):
       if 'paste' in request.session and request.session['paste']:
           paste = request.session['paste']
           print(paste.char_id)
           return render(request, self.template, {"paste": paste})
       else:
           print(' cant find paste')
           return render(request, self.template)

class DeletePaste(View):

   def post(self, request, char_id):
       try:
           paste = Paste.objects.get(char_id=char_id)
           paste.delete_paste()
       except ObjectDoesNotExist:
           render(request, "pastes/show_error.html", {"reason": "not_found"}, status=404)
       finally:
           return redirect("home:home")