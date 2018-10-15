from django.shortcuts import render,redirect
from django.views import View
from django.utils import timezone
from .query_utils import get_queryset

from django.views.generic import *
from home.models import Paste
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
# TODO: Add condition to fetch non expired pastes
class ShowPaste(View):
    template = "pastes/show_paste.html"

    # def get_queryset(self):
    #     return Paste.objects.filter(deleted=False).get(char_id=self.kwargs['char_id'])

    def get(self, request, char_id):
        try:
            paste = get_queryset(self)
        except ObjectDoesNotExist:
            print('something went wrong')
            return render(request, "pastes/show_error.html", {"reason": "not_found"}, status=404)
        else:
            print(paste.char_id)
            # save current Paste in session
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
           try:
              paste = get_queryset(self)
           except ObjectDoesNotExist:
                return render(request, "pastes/show_error.html", { "reason": "not_found"}, status=404)
           else:
               return render(request, self.template, {"paste": paste})

class DeletePaste(View):

   def post(self, request, char_id):
       try:
           paste = Paste.objects.get(char_id=char_id)
           del request.session['paste']
       except ObjectDoesNotExist:
           render(request, "pastes/show_error.html", {"reason": "not_found"}, status=404)
       except KeyError:
           raise
       else:
           paste.delete_paste()
       finally:
           return redirect("home:home")