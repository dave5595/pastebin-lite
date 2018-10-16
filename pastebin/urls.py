from django.contrib import admin
from django.urls import path, include
from pastes import views as paste_views

urlpatterns = [
    path('', include('home.urls', 'home')),
    path('admin/', admin.site.urls),
    path('pastes/', paste_views.ShowQueryResults.as_view(), name="query_results"),
    path('pastes/<str:char_id>', paste_views.ShowPaste.as_view(), name="show_paste"),
    path('pastes/<str:char_id>/confirm_delete', paste_views.ConfirmDelete.as_view(), name="confirm_delete"),
    path('pastes/<str:char_id>/delete', paste_views.DeletePaste.as_view(), name='delete_paste'),
]
