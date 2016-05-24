from django.conf.urls import url

from .views import cart_count, CartView


urlpatterns = [
    url(r'^cart/$', CartView.as_view(), name='cart_cart'),
    url(r'^count/$', cart_count, name='cart_count'),
]
