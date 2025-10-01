from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib import messages
from .models import Conversation, Message
from .services import AIService
import json


@login_required
def home(request):
    """Main chat interface"""
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')[:10]
    
    # Check if a specific conversation is requested
    conversation_id = request.GET.get('conversation')
    active_conversation = None
    
    if conversation_id:
        try:
            active_conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            pass
    
    # Check if chat interface is forced (from Chat nav link)
    force_chat = request.GET.get('force_chat')
    
    # If forcing chat interface but no specific conversation, use the most recent one or create new one
    if force_chat and not active_conversation:
        if conversations.exists():
            active_conversation = conversations.first()
        # For new users with no conversations, force_chat=1 will still show chat interface
        # but with no active_conversation, which will show the welcome message in chat layout
    
    context = {
        'conversations': conversations,
        'active_conversation': active_conversation,
        'messages': active_conversation.messages.all() if active_conversation else [],
        'force_chat': force_chat,  # Pass this to template for logic
    }
    return render(request, 'chat/home.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """View specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversations = Conversation.objects.filter(user=request.user)[:10]
    
    context = {
        'conversations': conversations,
        'active_conversation': conversation,
        'messages': conversation.messages.all(),
    }
    return render(request, 'chat/home.html', context)


@login_required
@csrf_exempt
def new_conversation(request):
    """Create a new conversation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation = Conversation.objects.create(user=request.user)
            
            # If initial message is provided, process it
            initial_message = data.get('initial_message')
            if initial_message:
                # Create user message
                user_message = Message.objects.create(
                    conversation=conversation,
                    content=initial_message,
                    is_from_user=True
                )
                
                # Generate AI response
                ai_service = AIService()
                try:
                    ai_response = ai_service.generate_response(initial_message)
                    Message.objects.create(
                        conversation=conversation,
                        content=ai_response,
                        is_from_user=False
                    )
                except Exception as e:
                    print(f"AI service error: {e}")
                    ai_response = "I'm sorry, I'm having trouble responding right now. Please try again later."
                    Message.objects.create(
                        conversation=conversation,
                        content=ai_response,
                        is_from_user=False
                    )
            
            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    else:
        # Handle GET request - redirect to home without creating conversation
        # This allows the UI to show the "new chat" interface
        return redirect('chat:home')


@login_required
@csrf_exempt
def send_message(request):
    """Send a message and get AI response"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message_content:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(user=request.user)
        
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
        
        # Update conversation title if it's the first message
        if not conversation.title:
            conversation.title = ai_service.generate_conversation_title(message_content)
            conversation.save()
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat(),
            },
            'ai_message': {
                'id': ai_message.id,
                'content': ai_message.content,
                'created_at': ai_message.created_at.isoformat(),
            },
            'conversation_title': conversation.title,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversation.delete()
    # Notification removed per user request
    return redirect('chat:home')


@login_required
@csrf_exempt
def api_delete_conversation(request, conversation_id):
    """API endpoint to delete a conversation"""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        conversation.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


class ConversationListView(ListView):
    """List all conversations for the user"""
    model = Conversation
    template_name = 'chat/conversation_list.html'
    context_object_name = 'conversations'
    paginate_by = 20
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)