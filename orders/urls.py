# from django.urls import path
# from .views import OrderView, CheckoutView, LatestOrderView

# urlpatterns = [
#     path('', OrderView.as_view(), name='orders'),          # GET / POST all orders
#     path('checkout/', CheckoutView.as_view(), name='checkout'),  # POST checkout
#     path('latest/', LatestOrderView.as_view(), name='latest-order'), # GET latest
# ]
from django.urls import path
from .views import (
    OrderView,
    LatestOrderView,
    create_razorpay_order,
    verify_razorpay_payment
)

urlpatterns = [
    path('', OrderView.as_view(), name='orders'),                    # GET / POST all orders
    path('latest/', LatestOrderView.as_view(), name='latest-order'), # GET latest order

    # Razorpay endpoints
    path('payments/create-order/', create_razorpay_order, name='razorpay-create-order'),
    path('payments/verify/', verify_razorpay_payment, name='razorpay-verify'),
]
