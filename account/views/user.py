from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from account.serializers import EndUserSerializer
from account.models import EndUser
from account.renderers import UserRenderer


class UserRetrieveView(generics.RetrieveUpdateAPIView):
    lookup_field = 'username'
    renderer_classes = [UserRenderer]
    queryset = EndUser.objects.all()
    serializer_class = EndUserSerializer
    permission_classes = [IsAuthenticated]
