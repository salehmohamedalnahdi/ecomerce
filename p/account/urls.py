from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    
    path('signup',views.signup , name='signup' ),
    path('profile/<slug:slug>',views.profile , name='profiles' ),
    #path('profile',views.profile , name='profiles' ),
  
]


