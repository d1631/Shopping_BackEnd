from rest_framework import routers

from api_vouchers.views import VoucherViewSet

app_name = 'api_vouchers'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'', VoucherViewSet, basename='voucher')
urlpatterns = router.urls
