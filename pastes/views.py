from django.shortcuts import render,redirect
from gen_utils import generate_random_char_id
from django.views.generic import *
from home.models import Paste
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class ShowPaste(View):
    template = "pastes/show_paste.html"
    def get(self, request, char_id):
        try:
            paste = Paste().get_paste_by_id(False, char_id)
        except ObjectDoesNotExist:
            print('something went wrong')
            return render(request, "pastes/show_error.html", {"reason": "not_found"}, status=404)
        else:
            # save current Paste in session
            request.session['paste'] = paste
            #  if client_id key exist do nothing and return the template
            if 'client_id' in request.session:
                return render(request, self.template, {"paste": paste, "paste_text": paste.text})
            else:
                #    create a uniq key for the user in db
                #    set it to the session
                #    increment the hits prop of the paste
                #    return the current paste
                client_id = generate_random_char_id()
                request.session['client_id'] = client_id
                # session will reset every time you restart the application
                # expect paste to increment on app boot success or visit with another browser
                # expect paste to not increment if opened on additional tabs on the SAME browser
                Paste.increment_hits(paste)
                return render(request, self.template, {"paste": paste, "paste_text": paste.text})


class ShowQueryResults(View):
    template = "pastes/queried_paste_results.html"

    def get(self, request):
        context_dict = {}
        query = request.GET['q']
        pastes = Paste().get_pastes_by_query_string(False, query)

        if not pastes:
            context_dict['no_results'] = query
        else:
            context_dict['pastes'] = pastes
            context_dict['query'] = query
        return render(request, self.template, context_dict)

class ConfirmDelete(View):
   template = "pastes/confirm_delete_paste.html"
   error_template = "pastes/show_error.html"

   def get(self, request, char_id):
       if 'paste' in request.session and request.session['paste']:
           paste = request.session['paste']
           return render(request, self.template, {"paste": paste})
       else:
           try:
              paste = Paste().get_paste_by_id(False, char_id)
           except ObjectDoesNotExist:
                return render(request, self.error_template , { "reason": "not_found"}, status=404)
           else:
               return render(request, self.template, {"paste": paste })

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