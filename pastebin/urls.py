from django.contrib import admin
from django.urls import path, include
from pastes import views as paste_views

urlpatterns = [
    path('', include('home.urls', 'home')),
    path('admin/', admin.site.urls),
    path('pastes/<str:char_id>', paste_views.ShowPaste.as_view(), name="show_paste")
]
