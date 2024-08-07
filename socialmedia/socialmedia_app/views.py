from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser as User
from .models import FriendRequest, Friend
from .serializers import (
    UserSignupSerializer,
    UserSearchSerializer,
    FriendRequestCreateSerializer,
    HandleFriendRequestSerializer,
    FriendRequestSerializer,
    FriendSerializer,
)
from .utils import (
    CustomPageNumberPagination,
    CustomUserRateThrottle
)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = super().post(request, *args, **kwargs)
        if serializer.data:
            return Response({"data": "User Created successfully"}, status=201)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.hash_password(serializer.instance)

    def hash_password(self, serializer_obj):
        serializer_obj.password = make_password(serializer_obj.password)
        serializer_obj.save(update_fields=['password'])
        return serializer_obj


class SearchUsersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSearchSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']


class SendFriendRequestView(APIView):
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendRequestCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Friend request sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HandleFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        friend_request_id = request.data.get('id')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HandleFriendRequestSerializer(
            instance=friend_request,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            updated_request = serializer.save()
            _status = updated_request.status
            return Response({"message": f"Friend request has been {_status}"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(user=user)


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')
