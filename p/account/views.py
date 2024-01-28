from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from django.contrib.auth import login , authenticate,logout
from .models import Profile
#from .forms import Userform , Profileform,Signupform
from django.contrib.auth.decorators import login_required
from products.models import Myfavorite
from django.contrib.auth.models import User
from django.views.generic import View,ListView,UpdateView,DeleteView,FormView,CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django_countries.fields import CountryField
# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('/products')

    else:
        form = UserCreationForm()

    context = {'form' : form}
    return render(request , 'registration/signup.html' , context)

@login_required(login_url='/account/login/')
def profile(request, slug):
    choices=CountryField().choices + [('', 'Select Country')]
    profile = get_object_or_404(Profile, slug=slug)
    order_user=Myfavorite.objects.filter(u=request.user) 
    if 'images' in request.FILES: 
        if len(request.FILES)!=0:
          i=request.FILES['images']
          profile.image=i
          profile.save()
    if 'c' in request.POST: 
        country=request.POST["c"]
        profile.country=country
        profile.save() 

    if "address" in request.POST or 'email' in request.POST:
        a=request.POST["address"]
        e=request.POST['email']
        if a:
          profile.address=a
        if e:
          u=User.objects.get(username=request.user)
          u.email=e
          u.save()
        profile.save()

    context = {'profile' : profile,'order_user':order_user,'choices':choices}
    return render(request , 'profile.html', context)

  


