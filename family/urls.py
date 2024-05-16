from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user, name='user'),
    path('familytree/', views.familytree, name='familytree'),
    path('events/', views.events, name='events'),
    path('viewevents/', views.event_list, name='event_list'),
    path('addevent/', views.add_event, name='add_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)