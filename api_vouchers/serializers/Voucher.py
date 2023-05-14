from rest_framework import serializers

from api_vouchers.models import Voucher


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ['name', 'rate']
