from django.conf.urls import url

from .views import cart_count, CartView, ItemDetail


urlpatterns = [
    url(r'^cart/$', CartView.as_view(), name='cart_cart'),
    url(r'^count/$', cart_count, name='cart_count'),
    url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='cart_item'),
]
