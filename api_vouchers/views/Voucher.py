from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_vouchers.models import Voucher
from api_vouchers.serializers import VoucherSerializer
from api_base.views import MyBaseViewSet


class VoucherViewSet(MyBaseViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    permission_map = {}
    serializer_map = {}
