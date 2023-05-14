from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core import settings

# from django.conf.urls import url
# from django.conf import settings
# from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),
    # url(r'^media/(?P<path>.")$', serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.")$', serve, {'document_root': settings.STATIC_ROOT}),
    path('product/', include('api_products.urls')),
    path('category/', include('api_categories.urls')),
    path('user/', include('api_users.urls')),
    path('account/', include('api_accounts.urls')),
    path('order/', include('api_orders.urls')),
    path('voucher/', include('api_vouchers.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
