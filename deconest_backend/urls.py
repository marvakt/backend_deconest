from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # User authentication
    path('api/users/', include('users.urls')),

    # Product APIs
    path('api/products/', include('products.urls')),

    # Wishlist APIs
    path('api/wishlist/', include('wishlist.urls')),

    # Cart APIs
    path('api/cart/', include('cart.urls')),

    # Order APIs
    path('api/orders/', include('orders.urls')),

    # Admin panel APIs
    path('api/adminpanel/', include('adminpanel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
