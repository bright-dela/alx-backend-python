from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id", "username", "first_name", "last_name",
            "email", "phone_number", "role", "created_at", "password"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def validate_phone_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  

    class Meta:
        model = Message
        fields = ["message_id", "sender", "conversation", "message_body", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages", "created_at"]

    def get_messages(self, obj):
        """Return nested messages within the conversation"""
        messages = obj.messages.all().order_by("sent_at")
        return MessageSerializer(messages, many=True).data
