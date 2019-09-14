from django.urls import path
from MyAdmin.views import homepage, loginView, logout_view, mainmenu, register, about,baseexample
from django.contrib.auth.decorators import login_required

app_name = 'MyAdmin'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('About/', about, name='About'),
    path('clogin/', loginView, name='clogin'),
    path('log-out/', logout_view, name='logout'),
    path("Newregister/", register, name="register"),
    path('mainmenu/', mainmenu , name='mainmenu'),
path('baseexample/', baseexample , name='baseexample'),

     ]