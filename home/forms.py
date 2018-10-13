from django import forms
from .models import Paste

# TODO: read up on django forms!

class SubmitPasteForm(forms.Form):
    """ Form to submit the paste. Contains paste text, title and optionally, time until expiration"""
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
                            widget=forms.TextInput(attrs={"placeholder": "Untitled"}))
    text = forms.CharField(min_length=1,
                           max_length=100000,
                           error_messages={"required": "The paste can't be empty."})
    expiration = forms.ChoiceField(choices=EXPIRATION_CHOICES)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        if self.request == None:
            raise AttributeError(
                "'%s' requires a valid Django request object as its request parameter" % self.__class__.__name__)

        super(SubmitPasteForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        """Replace the title with Untitled if it is not provided"""
        title = self.cleaned_data.get("title")
        # If user provides an empty title, replace it with Untitled
        if title.strip() == "":
            title = "Untitled"
        return title

    def clean_text(self):
        """Check that the user hasn't uploaded too many pastes"""
        return self.cleaned_data.get("text")