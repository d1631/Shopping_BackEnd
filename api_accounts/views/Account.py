from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from api_accounts.constants import RoleData
from api_accounts.models import Account
from api_accounts.models import Role
from api_users.models import User
from api_accounts.serializers import AccountSerializer
from api_accounts.services import AccountService
from api_base.views import MyBaseViewSet
from api_users.serializers import UserSerializer
import os
import uuid
import datetime


class AccountViewSet(MyBaseViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    serializer_map = {}
    permission_map = {}

    @action(methods=['post'], detail=False)
    @transaction.atomic
    def sign_up(self, request):
        user_data = request.data
        is_existed = Account.objects.filter(username=user_data.get(
            'username')) or User.objects.filter(email=user_data.get('email'))
        if is_existed:
            return Response({"message": "Username already exists"}, status=status.HTTP_403_FORBIDDEN)
        user_data._mutable = True
        user_data["role"] = RoleData.USER.value.get("id")
        user_data._mutable = False
        account_serializer = AccountSerializer(data=user_data)
        if account_serializer.is_valid(raise_exception=True):
            account = account_serializer.save()
            user_data._mutable = True
            user_data['account'] = account.id.hex
            user_data._mutable = False
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        account = Account.objects.filter(username=username)
        if account.exists():
            account = account.first()
            #{"username":"aaaa", "password":"1234"}
            if not account.is_activate:
                return Response({"Message": "Account has been deactivated!"}, status=status.HTTP_400_BAD_REQUEST)
            if check_password(password, account.password):
                # return Response(self.serializer_class(account).data, status=status.HTTP_200_OK)
                token = RefreshToken.for_user(account)
                response = {
                    'access_token': str(token.access_token),
                    'refreshToken': str(token),
                    'user_id': AccountService.get_user_id(account)
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response({"message": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login_with_google(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        new_account = None
        if user.exists():
            user = user.first()
            new_account = user.account
            if not new_account.is_activate:
                return Response({"Message": "Account has been deactivated!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_account = Account.objects.create(username=email, password=make_password(os.getenv(
                'DEFAULT_ADMIN_PASSWORD')), role=Role.objects.get(name=RoleData.USER.name))
            new_user = User.objects.create(name=name, phone=None, birthday=None,
                                           email=email, gender="Male", account=new_account)
        token = RefreshToken.for_user(new_account)
        response = {
            'access_token': str(token.access_token),
            'refreshToken': str(token),
            'user_id': AccountService.get_user_id(new_account)
        }
        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login_with_facebook(self, request):
        us_id = request.data.get('id')
        name = request.data.get('name')
        user = User.objects.filter(email=us_id)
        new_account = None
        if user.exists():
            user = user.first()
            new_account = user.account
            if not new_account.is_activate:
                return Response({"Message": "Account has been deactivated!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_account = Account.objects.create(username=us_id, password=make_password(os.getenv(
                'DEFAULT_ADMIN_PASSWORD')), role=Role.objects.get(name=RoleData.USER.name))
            new_user = User.objects.create(
                name=name, phone=None, birthday=None, email=us_id, gender="Male", account=new_account)
        token = RefreshToken.for_user(new_account)
        response = {
            'access_token': str(token.access_token),
            'refreshToken': str(token),
            'user_id': AccountService.get_user_id(new_account)
        }
        return Response(response, status=status.HTTP_200_OK)
