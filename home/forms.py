from django import forms
from .models import Paste

class SubmitPasteForm(forms.Form):
    EXPIRATION_CHOICES = (
        (Paste.NEVER, "Never"),
        (Paste.FIFTEEN_MINUTES, "15 minutes"),
        (Paste.ONE_HOUR, "1 hour"),
        (Paste.ONE_DAY, "1 day"),
        (Paste.ONE_WEEK, "1 week"),
        (Paste.ONE_MONTH, "1 month"),
    )

    title = forms.CharField(max_length=128,
                            required=False,
                            widget=forms.TextInput(attrs={"placeholder": "Untitled", "class": 'form-control'}))

    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'paste-text-field'}),
                            min_length=1,
                           max_length=100000,
                           error_messages={"required": "The paste can't be empty."})

    expiration = forms.ChoiceField(widget=forms.Select(attrs={"class": 'form-control'}), choices=EXPIRATION_CHOICES)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        # If user provides an empty title, replace it with Untitled
        if title.strip() == "":
            title = "Untitled"
        return title

    def clean_text(self):
        return self.cleaned_data.get("text")
