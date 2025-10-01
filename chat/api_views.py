from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .services import AIService


class ConversationViewSet(viewsets.ModelViewSet):
    """API ViewSet for conversations"""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message to the conversation"""
        conversation = self.get_object()
        message_content = request.data.get('message', '').strip()
        
        if not message_content:
            return Response({'error': 'Message cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            content=message_content,
            is_from_user=True
        )
        
        # Generate AI response
        ai_service = AIService()
        conversation_history = conversation.messages.order_by('created_at')
        ai_response = ai_service.generate_response(message_content, conversation_history)
        
        # Save AI response
        ai_message = Message.objects.create(
            conversation=conversation,
            content=ai_response,
            is_from_user=False
        )
        
        return Response({
            'user_message': MessageSerializer(user_message).data,
            'ai_message': MessageSerializer(ai_message).data,
        })


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for messages"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(conversation__user=self.request.user)