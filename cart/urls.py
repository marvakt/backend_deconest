# from django.urls import path
# from .views import CartView, ClearCartView

# urlpatterns = [
#     path('', CartView.as_view(), name='cart'),
#     path('<int:pk>/', CartView.as_view(), name='cart-detail'),
#     path('clear/', ClearCartView.as_view(), name='cart-clear'),
# ]


from django.urls import path
from .views import CartView, ClearCartView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),             # GET all / POST add
    path("<int:pk>/", CartView.as_view(), name="cart-detail"),  # PUT/DELETE single item
    path("clear/", ClearCartView.as_view(), name="cart-clear"), # DELETE all
]

