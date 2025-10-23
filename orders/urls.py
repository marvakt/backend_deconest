from django.urls import path
from .views import OrderView, CheckoutView, LatestOrderView

urlpatterns = [
    path('', OrderView.as_view(), name='orders'),          # GET / POST all orders
    path('checkout/', CheckoutView.as_view(), name='checkout'),  # POST checkout
    path('latest/', LatestOrderView.as_view(), name='latest-order'), # GET latest
]
