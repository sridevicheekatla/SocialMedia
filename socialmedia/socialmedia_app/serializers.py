from rest_framework import serializers

from .models import CustomUser, FriendRequest, Friend


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', ]


class UserSignupSerializer(UserSearchSerializer):
    class Meta:
        model = CustomUser
        fields = UserSearchSerializer.Meta.fields + ['id', 'password']


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['to_user', ]

    def validate_to_user(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError({"message": "You cannot send a friend request to yourself."})
        try:
            CustomUser.objects.get(id=value.id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found."})
        return value

    def create(self, validated_data):
        from_user = self.context['request'].user
        to_user = validated_data['to_user']

        if self.Meta.model.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError({"message": "Friend request already sent"})

        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return friend_request


class HandleFriendRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=['accepted', 'rejected'])

    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError({'error': 'Status must be either accepted or rejected'})
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.EmailField(source='from_user.email')
    to_user = serializers.EmailField(source='to_user.email')

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status',]


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSearchSerializer()

    class Meta:
        model = Friend
        fields = ['friend', ]
