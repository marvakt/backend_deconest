

from django.urls import path
from .views import (
    OrderView,
    LatestOrderView,
    create_razorpay_order,
    verify_razorpay_payment
)

urlpatterns = [
    path('', OrderView.as_view(), name='orders'),                   
    path('latest/', LatestOrderView.as_view(), name='latest-order'), 

    # Razorpay endpoints
    path('payments/create-order/', create_razorpay_order, name='razorpay-create-order'),
    path('payments/verify/', verify_razorpay_payment, name='razorpay-verify'),
]
