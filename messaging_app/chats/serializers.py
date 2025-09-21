from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'password']
        read_only_fields = ['created_at', 'id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)
    conversation_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_id', 'conversation_id', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at', 'sender', 'conversation']

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id', None)
        conversation_id = validated_data.pop('conversation_id', None)

        if sender_id:
            sender = User.objects.get(id=sender_id)
        else:
            request = self.context.get('request', None)
            sender = getattr(request, 'user', None)

        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            conversation = self.context.get('conversation', None)

        message = Message.objects.create(sender=sender, conversation=conversation, **validated_data)
        return message


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False,
        help_text="List of user UUIDs to be participants in the conversation"
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_ids', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at', 'messages', 'participants']

    def create(self, validated_data):
        participants_ids = validated_data.pop('participants_ids', None) or []
        conversation = Conversation.objects.create(**validated_data)
        if participants_ids:
            users = User.objects.filter(id__in=participants_ids)
            conversation.participants.set(users)
        return conversation

    def update(self, instance, validated_data):
        participants_ids = validated_data.pop('participants_ids', None)
        if participants_ids is not None:
            users = User.objects.filter(id__in=participants_ids)
            instance.participants.set(users)
        instance.save()
        return instance
