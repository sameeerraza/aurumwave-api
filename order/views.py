from django.core.mail import send_mail
from rest_framework import response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from product.models import Product
from .serializers import OrderSerializer


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Require JWT authentication

    def post(self, request):
        user = request.user
        try:
            serializer = OrderSerializer(data=request.data, context={"request": request})

            if serializer.is_valid():
                order = serializer.save()
                message = (f"Congratulation, {user.username}, your order placed, you will get an email when we will accept it.\n"
                           f"Your order number is {order.id}")

                send_mail(
                    "Order Status",
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )

                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return response.Response(
                data={"error": "No product found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
