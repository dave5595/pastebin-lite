from django.shortcuts import render, redirect
from .models import Paste
from .forms import SubmitPasteForm
from django.views import View

class HomeView(View):
    form_class = SubmitPasteForm
    template = "home/home.html"
    paste = Paste()
    def get(self, request):
        form = self.form_class()
        latest_pastes = Paste().get_pastes(include_expired=False)
        return render(request, self.template, {'form': form, 'latest_pastes': latest_pastes})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            paste_data = form.cleaned_data
            char_id =Paste().add_paste(title=paste_data["title"],
                                          text=paste_data["text"],
                                          expiration=paste_data["expiration"],)
            # Redirect to the newly created paste
            return redirect("show_paste", char_id=char_id)

        return render(request, self.template, {'form': form})