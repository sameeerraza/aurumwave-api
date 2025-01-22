from django.db.models import Q
from rest_framework import generics, response, status
from rest_framework.permissions import IsAuthenticated

from account.renderers import UserRenderer
from product.models import Product
from product.serializers import (
    RequestListCreateSerializer,
)


# from django.conf.settings import EMAIL_HOST_USER


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = RequestListCreateSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def filter_with_params(self, request, requests):
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")
        country = request.query_params.get("country")
        city = request.query_params.get("city")

        if search:
            requests = requests.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if ordering:
            requests = requests.order_by(ordering)
        if city:
            requests = requests.filter(city=city)
        if country:
            requests = requests.filter(country=country)

        return requests

    def get(self, request):
        try:
            requests = self.get_queryset()
            user = request.user
            # requests = requests.filter(is_ordered=False).exclude(user=user)
            requests = self.filter_with_params(request, requests)

            if not requests:
                return response.Response(
                    "No requests found.", status=status.HTTP_204_NO_CONTENT
                )

            ser = self.serializer_class(requests, many=True)

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
    lookup_url_kwarg = "request_id"
    serializer_class = RequestListCreateSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()