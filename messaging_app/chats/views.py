from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, id=user_id)
        conversation.participants.add(user)
        return Response(self.get_serializer(conversation).data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        conversation_id = self.request.data.get('conversation_id') or self.request.query_params.get('conversation_id')
        if conversation_id:
            try:
                ctx['conversation'] = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                ctx['conversation'] = None
        return ctx

    def create(self, request, *args, **kwargs):
        """
        Create a message. Prefer using request.user as sender; otherwise accept sender_id in payload.
        Require conversation_id in payload or query string.
        """
        data = request.data.copy()

        conversation_id = data.get('conversation_id')
        if not conversation_id:
            return Response({'detail': 'conversation_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user and getattr(request.user, 'is_authenticated', False):
            data['sender_id'] = str(request.user.id)

        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        conv = get_object_or_404(Conversation, id=conversation_id)

        message = Message.objects.create(
            sender=User.objects.get(id=serializer.validated_data.get('sender_id')) if serializer.validated_data.get('sender_id') else request.user,
            conversation=conv,
            message_body=serializer.validated_data['message_body']
        )
        out_serializer = self.get_serializer(message)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        conversation_id = request.query_params.get('conversation_id')
        qs = self.get_queryset()
        if conversation_id:
            qs = qs.filter(conversation__id=conversation_id).order_by('sent_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

