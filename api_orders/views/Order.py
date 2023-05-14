import os

import stripe
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_accounts.services import AccountService
from api_base.views import MyBaseViewSet
from api_orders.models import Order
from api_orders.serializers import OrderSerializer
from api_orders.serializers.Order import MyOrderSerializer
from api_vouchers.models import Voucher
load_dotenv()


class OrderViewSet(MyBaseViewSet):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializer
    permission_map = {}
    serializer_map = {}

    @action(methods=['post'], detail=False)
    def checkout(self, request):
        http_authorization = str(request.META.get('HTTP_AUTHORIZATION'))
        token = AccountService.get_token(http_authorization)
        account = AccountService.get_account_by_token(token)
        serializer = OrderSerializer(data=request.data)
        voucher = Voucher.objects.filter(name=request.data.get('voucher'))
        if voucher.exists():
            voucher = voucher.first()
            rate = voucher.rate if voucher.rate != None else 0
        if serializer.is_valid():
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
            paid_amount = sum(
                item.get('quantity') * item.get('product').price for item in serializer.validated_data['items']) * (1 - rate)
            try:
                charge = stripe.Charge.create(
                    amount=int(paid_amount * 100),
                    currency='USD',
                    description='Charge from Djackets',
                    source=serializer.validated_data['stripe_token']
                )
                order = serializer.save(
                    account=account, paid_amount=paid_amount)
                return Response(MyOrderSerializer(order).data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def your_order(self, request):
        http_authorization = str(request.META.get('HTTP_AUTHORIZATION'))
        token = AccountService.get_token(http_authorization)
        account = AccountService.get_account_by_token(token)
        orders = Order.objects.filter(account=account)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
