from django.contrib import admin
from .models import Product,Cat,Myfavorite,Order,Orderdetails,Comment
def re_is_finshied_to_true(modeladmin,request,queryset):
    queryset.update(is_finshied=True)
#re_is_finshied_to_true.short_description='change'
class OAdmin(admin.ModelAdmin):
    list_display=['user','is_finshied','date']
    list_filter=['user','date']
    search_fields=['user','is_finshied','date']
    actions = [re_is_finshied_to_true]

class CommentAdmin(admin.ModelAdmin):
    list_display=['name_product','user_comment','comment','date','rate']

admin.site.register(Product)
admin.site.register(Cat)
admin.site.register(Myfavorite)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Order,OAdmin)
admin.site.register(Orderdetails)


# Register your models here.
