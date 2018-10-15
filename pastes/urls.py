from django.urls import path
from . import views

app_name = "pastes"

urlpatterns = [
    path('paste/<str:char_id/delete>', views.DeletePaste.as_view(), name='delete_paste'),
]