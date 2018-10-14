from django.urls import path
from . import views

app_name = "pastes"

urlpatterns = [
    path('', views.ShowPaste.as_view(), name='show-pastes')
]