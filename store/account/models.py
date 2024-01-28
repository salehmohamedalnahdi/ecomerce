from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import datetime
from django_countries.fields import CountryField
from django.utils.text import slugify

from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='photo/%y/%m/%d',blank=True, null=True)#upload_to='photo/%y/%m/%d',
    country = models.CharField(max_length=200,blank=True, null=True, choices=CountryField().choices + [('', 'Select Country')])
    address = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.DateTimeField(default = datetime.datetime.now)


    def save(self , *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.user.username)
        super(Profile, self).save( *args , **kwargs)


    class Meta:
        #abstract = True
        verbose_name =("Profiless")
        #verbose_name_plural = _("Profiles")

    def get_absolute_url(self):
        return reverse("account:profiles", kwargs={"slug": self.slug})
    
    def __str__(self):
        return str(self.user)
     
def create_profile(sender , **kwargs):
    #print(kwargs)
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile , sender=User)

        
# Create your models here.
