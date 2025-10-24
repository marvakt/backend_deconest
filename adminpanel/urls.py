# from django.urls import path
# from .views import (
#     AdminUserListView, AdminUserBlockView, AdminUserUnblockView,
#     AdminProductListCreateView, AdminProductDetailView, AdminProductArchiveView, AdminProductUnarchiveView,
#     AdminOrderListView, AdminOrderTotalRevenueView, AdminOrderTotalProductsSoldView
# )

# urlpatterns = [
#     # User management
#     path('users/', AdminUserListView.as_view(), name='admin-users'),
#     path('users/<int:pk>/block/', AdminUserBlockView.as_view(), name='admin-user-block'),
#     path('users/<int:pk>/unblock/', AdminUserUnblockView.as_view(), name='admin-user-unblock'),

#     # Product management
#     path('products/', AdminProductListCreateView.as_view(), name='admin-products'),
#     path('products/<int:pk>/', AdminProductDetailView.as_view(), name='admin-product-detail'),
#     path('products/<int:pk>/archive/', AdminProductArchiveView.as_view(), name='admin-product-archive'),
#     path('products/<int:pk>/unarchive/', AdminProductUnarchiveView.as_view(), name='admin-product-unarchive'),

#     # Orders
#     path('orders/', AdminOrderListView.as_view(), name='admin-orders'),
#     path('orders/total-revenue/', AdminOrderTotalRevenueView.as_view(), name='admin-orders-total-revenue'),
#     path('orders/total-products-sold/', AdminOrderTotalProductsSoldView.as_view(), name='admin-orders-total-products-sold'),
# ]



from django.urls import path
from .views import (
    AdminUserListView, AdminUserBlockView, AdminUserUnblockView,
    AdminProductListCreateView, AdminProductDetailView, AdminProductArchiveView, AdminProductUnarchiveView,
    AdminOrderListView, AdminOrderDetailView, AdminOrderTotalRevenueView, AdminOrderTotalProductsSoldView
)

urlpatterns = [
    # User management
    path('users/', AdminUserListView.as_view(), name='admin-users'),
    path('users/<int:pk>/block/', AdminUserBlockView.as_view(), name='admin-user-block'),
    path('users/<int:pk>/unblock/', AdminUserUnblockView.as_view(), name='admin-user-unblock'),

    # Product management
    path('products/', AdminProductListCreateView.as_view(), name='admin-products'),
    path('products/<int:pk>/', AdminProductDetailView.as_view(), name='admin-product-detail'),
    path('products/<int:pk>/archive/', AdminProductArchiveView.as_view(), name='admin-product-archive'),
    path('products/<int:pk>/unarchive/', AdminProductUnarchiveView.as_view(), name='admin-product-unarchive'),

    # Orders
    path('orders/', AdminOrderListView.as_view(), name='admin-orders'),
    path('orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),  # <-- added
    path('orders/total-revenue/', AdminOrderTotalRevenueView.as_view(), name='admin-orders-total-revenue'),
    path('orders/total-products-sold/', AdminOrderTotalProductsSoldView.as_view(), name='admin-orders-total-products-sold'),
]
