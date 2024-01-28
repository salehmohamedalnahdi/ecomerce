from.models import *
import django_filters
from django.utils.translation import gettext_lazy as _

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model=Product
        fields=['pcat']
        #labels = {'pcat': _('Categoery'),}
        #help_texts = {'pcat': _('Some useful help text.'),}
