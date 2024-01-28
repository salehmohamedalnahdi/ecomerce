from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Myfavorite,Order,Orderdetails,Payment,Comment
from django.core.paginator import Paginator
from .filters import OrderFilter 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View,ListView,DetailView
from django.utils.decorators import method_decorator
from account.forms import Checkoutform

def products(request):
    u1=None
    pp=Product.objects.all()
    if 'search' in request.GET:
       u1=request.GET['search']
       pp=pp.filter(pname__icontains=u1)
    myfilter=OrderFilter(request.GET,queryset=pp)
    pp=myfilter.qs
    
    paginator=Paginator(pp,3)
    page=request.GET.get('page')
    p=paginator.get_page(page)

    return render(request, 'products/index.html',{'p':p,'myfilter':myfilter})
"""
def index2(request):
   u1=None
   pp=Product.objects.all()
   if 'search' in request.GET:
       u1=request.GET['search']
       pp=pp.filter(pname__icontains=u1)
   myfilter=OrderFilter(request.GET,queryset=pp)
   pp=myfilter.qs
    
   paginator=Paginator(pp,1)
   page=request.GET.get('page')
   p=paginator.get_page(page)
   return render(request, 'products/index2.html',{'p':p,'myfilter':myfilter})
"""


class Detail(DetailView):
   model=Product
   template_name='products/product1.html'
   context_object_name='p'
   slug_field='pslug'

   def get_object(self):
      the_product=super().get_object()
      return the_product

   def get_context_data(self, **kwargs):
      context=super().get_context_data(**kwargs)
      total=0
      if Comment.objects.filter(name_product__pslug=self.get_object().pslug):
       show_comment=Comment.objects.filter(name_product__pslug=self.get_object().pslug)
       for i in show_comment:
          i=i.rate
          total+=i
       num=show_comment.count()
       total=total/num
       context['show_comment']=show_comment
      context['total']=total
      
      return context
   
   def post(self, request,*args, **kwargs):
      if Comment.objects.filter(name_product__pslug=self.get_object().pslug,user_comment=request.user).exists():
         f=Comment.objects.get(name_product__pslug=self.get_object().pslug,user_comment=request.user)
         if not f.comment:
          f.comment=request.POST['comment'] 
          f.save()
         return redirect('products:pro', slug=self.get_object().pslug)
      else:
         if not 'stars' in  request.POST:
            messages.info(request, "Plese Assess Prpject First")
            return redirect('products:pro', slug=self.get_object().pslug)
         else :
          f=Comment()
          f.user_comment=request.user
          f.comment=request.POST['comment'] or None
          f.name_product=self.get_object()
          f.rate=request.POST['stars']
          f.save()
          return redirect('products:pro', slug=self.get_object().pslug)


@login_required(login_url='/account/login/')
def add_to_fav(request, slug):
    product=Product.objects.get(pslug=slug)
    if Myfavorite.objects.filter(u=request.user,item__pslug=slug).exists():
          messages.info(request, "This Product Was Already Existed In Your Cart")
          return redirect('products:pro', slug=slug)

    else:
        myfavorite=Myfavorite.objects.create(u=request.user, item=product)
        myfavorite.save()
        messages.info(request, "This Product Was Aaded In Your Cart")
        return redirect('products:pro', slug=slug)


@login_required(login_url='/account/login/')
def remove_from_fav(request, slug):
    p= get_object_or_404(Product ,pslug=slug)
    if Myfavorite.objects.filter(u=request.user,item__pslug=slug).exists():
        Myfavorite.objects.get(u=request.user,item__pslug=slug).delete()
        messages.info(request, "Product Was Removed From Your Cart")
        return redirect('products:my_favproudcts')
    else:
      messages.info(request, "Product Was Not In Your Cart")
      return redirect('products:my_favproudcts')

@login_required(login_url='/account/login/')
def my_favorite_proudcts(request):
    order_user=Myfavorite.objects.filter(u=request.user)
    return render(request, 'products/my_favproudcts.html',{'order_user':order_user})

     
@login_required(login_url='/account/login/')     
def add_qty_to_order(request,id):
   o=Orderdetails.objects.get(id=id)
   if o.qty >=1:
      o.qty+=1
      o.save()
      return redirect('products:orders')
   
@login_required(login_url='/account/login/')   
def sub_qty_from_order(request,id):
   o=Orderdetails.objects.get(id=id)
   if o.qty >1:
      o.qty-=1
      o.save()
      return redirect('products:orders')
   else:
      return redirect('products:orders')
   

@login_required(login_url='/account/login/')
def add_favorite_product_to_order(request,slug):
   pro=get_object_or_404(Product,pslug=slug)
   if request.method=='GET':
      qty=request.GET['qty']
      if Order.objects.filter(user=request.user,is_finshied=False).exists():
         order=Order.objects.get(user=request.user,is_finshied=False)
         if Orderdetails.objects.filter(order=order,product=pro).exists():
            oldpro=Orderdetails.objects.get(order=order,product=pro)
            oldpro.qty+=int(qty)
            oldpro.save()
            messages.info(request, "This Product Was Aaded In Your Order")
            return redirect('products:my_favproudcts')
         else:
           Orderdetails.objects.create(order=order,product=pro,qty=qty)
           messages.info(request, "This Product Was Aaded In Your Order")
           return redirect('products:my_favproudcts')
      else:
         order=Order.objects.create(user=request.user)
         Orderdetails.objects.create(order=order,product=pro,qty=qty)
         messages.info(request, "This Product Was Aaded In Your Order")
         return redirect('products:my_favproudcts')

@login_required(login_url='/account/login/')      
def orders(request):
      if Order.objects.filter(user=request.user,is_finshied=False).exists():
        order=Order.objects.get(user=request.user,is_finshied=False)
        orders=Orderdetails.objects.filter(order=order)
        total=0
        for i in orders:
          m=i.total_price_for_each_prouduct()
          total+=m
          print('\u2B50')

      else:
         messages.info(request, "You Don't Have An Order")
         return redirect('products:my_favproudcts')

      return render(request,'products/my_orders.html',{'orders':orders,'total':total,'order':order})
      
     
@login_required(login_url='/account/login/')
def remove_from_order(request, slug):
    product= get_object_or_404(Product ,pslug=slug)
    order=Order.objects.get(user=request.user,is_finshied=False)
    if Orderdetails.objects.filter(order=order,product=product).exists():
        Orderdetails.objects.get(order=order,product=product).delete()
        messages.info(request, "Product Was Removed From Your Order")
        return redirect('products:orders')
    else:
      messages.info(request, "Product Was Not In Your Order")
      return redirect('products:orders')

@login_required(login_url='/account/login/')
def checkout(request):
   context=None
   if request.method=='POST' and'pay' in request.POST:
     if Order.objects.filter(user=request.user,is_finshied=False):
       order=Order.objects.get(user=request.user,is_finshied=False)
       ship_address=request.POST['ship_address']
       ship_phone=request.POST['ship_phone']
       card_number=request.POST['card_number']
       expire=request.POST['expire']
       security_code=request.POST['security_code']
       pay=Payment(order=order,shipment_address=ship_address,shipment_phone=ship_phone,card_number=card_number,expire=expire,security_code=security_code)
       pay.save()
       order.is_finshied=True
       order.save()
       messages.info(request, "Your Order Is Finshied")
       return redirect('products:checkout')
        
   else:
    total=0
    
    if Order.objects.filter(user=request.user,is_finshied=False):
      order=Order.objects.get(user=request.user,is_finshied=False)
      orderdetails=Orderdetails.objects.filter(order=order)
      num_product=orderdetails.count()
      for i in orderdetails:
        t=i.total_price_for_each_prouduct()
        total+=t
      context={'total':total,'order':order,'num_product':num_product,'orderdetails':orderdetails}

   return render (request,'products/checkout.html',context) 


@login_required(login_url='/account/login/')
def checkout3(request):
   context=None
   form=Checkoutform() 
   if request.method=='POST':
     if Order.objects.filter(user=request.user,is_finshied=False):
       order=Order.objects.get(user=request.user,is_finshied=False)
       form=Checkoutform(request.POST)
       if form.is_valid():
         forms=form.save(commit=False)
         forms.order=order
         forms.save()
         order.is_finshied=True
         order.save()
         messages.info(request, "Your Order Is Finshied")
         return redirect('products:checkout')
        
   else:
    total=0
    
    if Order.objects.filter(user=request.user,is_finshied=False):
      order=Order.objects.get(user=request.user,is_finshied=False)
      orderdetails=Orderdetails.objects.filter(order=order)
      num_product=orderdetails.count()
      for i in orderdetails:
        t=i.total_price_for_each_prouduct()
        total+=t
      context={'total':total,'order':order,'num_product':num_product,'orderdetails':orderdetails,'form':form}

   return render (request,'products/checkout2.html',context)
