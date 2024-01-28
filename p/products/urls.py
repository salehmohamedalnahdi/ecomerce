from . import views  
from django.urls import path 
app_name='products'

urlpatterns = [ 
    path('', views.products,name='home'),
    #path('index2/index2', views.index2,name='index2'),
    path('<slug:slug>',views.Detail.as_view(), name='pro'),
    path('add-to-fav/<slug:slug>',views.add_to_fav, name='add'),
    path('remove-from-fav/<slug:slug>',views.remove_from_fav, name='remove'),
    path('o/my_favproudcts', views.my_favorite_proudcts, name='my_favproudcts'),
    #path('increse/<slug:slug>',views.increse, name='increse'),
    path('adds/<int:id>',views.add_qty_to_order, name='adds'),
    path('sub/<int:id>',views.sub_qty_from_order, name='sub'),
    path('order/<slug:slug>',views.add_favorite_product_to_order, name='order'),
    path('o/orders' ,views.orders, name='orders'),
    path('remove_from_order/<slug:slug>',views.remove_from_order, name='remove_from_order'),   
    path('ooo/checkout',views.checkout, name='checkout'),
    path('ooo/checkout3',views.checkout3, name='checkout3'),
   # path('<int:id>', views.product, name='product'),
    #path('show', views.showcomment, name='show'),
    #path('<slug:slug>',views.pro, name='pro'),    
    #path('checkout2',views.Checkout2.as_view(), name='checkout2'),
 

    ]
#urlpatterns = [
    #path('product', views.product, name='product'),
    #path('', views.products, name='products'),
    #path('<int:id>', views.products1, name='products1'),

    #]increse