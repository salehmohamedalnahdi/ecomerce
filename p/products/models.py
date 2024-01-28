from django.db import models
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField

class Product(models.Model):
    pname=models.CharField(max_length=50)
    pdesc=models.TextField(null=True,blank=True)
    pprice=models.DecimalField(max_digits=6,decimal_places=2)
    pcost=models.DecimalField(max_digits=6,decimal_places=2)
    pdiscount=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    pactive=models.BooleanField(default=True, null=True,blank=True)
    pcreated=models.DateTimeField(default=datetime.now, null=True,blank=True)
    pcat=models.ForeignKey('Cat', on_delete=models.CASCADE, null=True,blank=True, related_name='cats')
    pimage=models.ImageField(upload_to='photo/%y/%m/%d', null=True, blank=True)
    pslug=models.SlugField(null=True,blank=True)
    pnew=models.BooleanField(default=True)
    pbestseller=models.BooleanField(default=False)
    #comment=models.CharField(max_length=50,null=True,blank=True)


    def save(self,*args, **kwargs):
        if not self.pslug:
            self.pslug=slugify(self.pname)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.pname
    def get_absolute_url(self):
        return reverse('products:pro', kwargs={'slug':self.pslug})
    
    def get_add_to_favorite_url(self):
        return reverse('products:add', kwargs={'slug':self.pslug})
        
    def get_remove_from_favorite_url(self):
        return reverse('products:remove', kwargs={'slug':self.pslug})
    
    def get_remove_from_order_url(self):
        return reverse('products:remove_from_order', kwargs={'slug':self.pslug})
   

class Cat(models.Model):
    cname=models.CharField(max_length=50)
    cparent=models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE)
    cdesc=models.TextField(null=True,blank=True)
    cimage=models.ImageField(upload_to='photo/%y/%m/%d')
    def __str__(self):
        return self.cname


    
class Myfavorite(models.Model):# this is user's favourit products
    #this class is assuemd named my favourit products but i forget that do let's consider it favourit products
    u=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='us')
    item=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        return str(self.u)

    
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="order_user")
    orderdetails=models.ManyToManyField(Product,through='Orderdetails')
    date=models.DateTimeField(auto_now_add=True)
    is_finshied=models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)
    
 
    
class Orderdetails(models.Model):
        order =models.ForeignKey(Order,on_delete=models.CASCADE, related_name="orderdetails_order")
        product =models.ForeignKey(Product,on_delete=models.CASCADE, related_name="orderdetails_product")
        qty=models.IntegerField()

        def __str__(self):
          return str(self.order.user)
        
        def total_price_for_each_prouduct(self):
         if self.product.pdiscount:
             return self.product.pdiscount*self.qty
         else:
             return self.product.pprice*self.qty
    

class Comment(models.Model):
    comment=models.CharField(max_length=400,null=True, blank=True)
    name_product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='names')
    user_comment=models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    date=models.DateTimeField(auto_now_add=True)
    rate=models.IntegerField()
    def __str__(self):
        return str(self.name_product)
    

        
        
   

class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    shipment_address=models.CharField(max_length=150)
    shipment_phone=models.CharField(max_length=50)
    card_number=CardNumberField()
    expire=CardExpiryField()
    security_code=SecurityCodeField()



# Create your models here.
