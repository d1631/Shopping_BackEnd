from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_base.views import MyBaseViewSet
from api_products.models import Product
from api_products.serializers import ProductSerializer


class ProductViewSet(MyBaseViewSet):
    ITEMS_PER_PAGE = 12
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    permission_map = {

    }
    serializer_map = {

    }

    # @action(methods=['post', 'get'], detail=False)
    # def search(self, request):
    #     query = request.data.get('query', '')
    #     if query:
    #         products = Product.objects.filter(
    #             Q(name__icontains=query) | Q(description__icontains=query))
    #         if products.exists():
    #             return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"products": []})

    # @action(methods=['post'], detail=False)
    # def sort(self, request):
    #     datas = request.data.get('prop-dir').split('-')
    #     prop = datas[0]
    #     direction = datas[1]
    #     if prop == 'name':
    #         if direction == 'asc':
    #             products = Product.objects.order_by('name')
    #         else:
    #             products = Product.objects.order_by('-name')
    #     elif prop == 'price':
    #         if direction == 'asc':
    #             products = Product.objects.order_by('price')
    #         else:
    #             products = Product.objects.order_by('-price')

    #     if products.exists():
    #         return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"products": []})

    # @action(methods=['post', 'get'], detail=False)
    # def paginate(self, request):
    #     page = int(request.query_params.get('page'))
    #     if page:
    #         offset = (page-1) * self.ITEMS_PER_PAGE
    #         products = Product.objects.all()[offset:offset+self.ITEMS_PER_PAGE]
    #         return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

    # @action(methods=['get', 'post'], detail=False)

    def list(self, request):
        query = request.GET.get('query')
        datas = request.GET.get('prop-dir')
        page = request.GET.get('page')
        # SEARCH
        if query != None:
            query_set = Product.objects.filter(
                (Q(name__icontains=query) | Q(description__icontains=query)))
        else:
            query_set = Product.objects.all()

        # SORT
        if datas != None and datas != '':
            datas = datas.split('-')
            prop = datas[0]
            direction = datas[1]
            if prop == 'name':
                if direction == 'asc':
                    query_set = query_set.order_by('name')
                else:
                    query_set = query_set.order_by('-name')
            elif prop == 'price':
                if direction == 'asc':
                    query_set = query_set.order_by('price')
                else:
                    query_set = query_set.order_by('-price')
        # PAGINATE
        if page != None:
            page = int(page)
            offset = (page-1) * self.ITEMS_PER_PAGE
            query_set = query_set[offset:offset+self.ITEMS_PER_PAGE]

        return Response(self.serializer_class(query_set, many=True).data,
                        status=status.HTTP_200_OK)
