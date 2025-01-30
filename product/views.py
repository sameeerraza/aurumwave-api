from django.db.models import Q
from rest_framework import generics, response, status
from rest_framework.permissions import IsAuthenticated

from account.renderers import UserRenderer
from product.models import Product
from product.serializers import (
    RequestListCreateSerializer,
)
from utils.ai_search import advance_search


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = RequestListCreateSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def filter_with_params(self, request, products):
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")
        is_advanced = request.query_params.get("advance", "false").lower() == "true"

        # If advanced search is enabled, use AI-based search
        if is_advanced and search:
            products = advance_search(search)
        elif search:
            # Simple search: filter by title or description
            products = products.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if ordering:
            products = products.order_by(ordering)

        return products

    def get(self, request):
        try:
            products = self.get_queryset()
            user = request.user
            products = self.filter_with_params(request, products)

            if not products:
                return response.Response(
                    "No products found.", status=status.HTTP_204_NO_CONTENT
                )

            ser = self.serializer_class(products, many=True)

            return response.Response(ser.data, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(
                data={
                    "error": ser.errors,
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "product_id"
    serializer_class = RequestListCreateSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
