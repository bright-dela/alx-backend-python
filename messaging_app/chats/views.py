from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__username", "participants__email"]

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants"""
        participants_ids = request.data.get("participants", [])
        if not participants_ids:
            return Response(
                {"error": "At least one participant is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        conversation = Conversation.objects.create()
        conversation.participants.set(participants_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("sent_at")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body", "sender__username"]

    def create(self, request, *args, **kwargs):
        """Send a message to an existing conversation"""
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        message = Message.objects.create(
            sender=request.user, conversation=conversation, message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
