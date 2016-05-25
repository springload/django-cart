from django.conf.urls import url

from .views import cart_count, CartView, ItemDetail, ItemList


urlpatterns = [
    url(r'^cart/$', CartView.as_view(), name='cart_cart'),
    url(r'^count/$', cart_count, name='cart_count'),
    url(r'^item/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='cart_item'),
    url(r'^items/$', ItemList.as_view(), name='cart_items'),
]
