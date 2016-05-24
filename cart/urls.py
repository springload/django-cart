from django.conf.urls import url
from .views import cart_count


urlpatterns = [
    url(r'^count/$', cart_count, name='cart_count'),
]
