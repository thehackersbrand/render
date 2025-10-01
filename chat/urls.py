from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('send/', views.send_message, name='send_message'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation_list'),
    # API endpoints for AJAX calls
    path('api/conversations/', views.new_conversation, name='api_new_conversation'),
    path('api/conversations/<int:conversation_id>/messages/', views.send_message, name='api_send_message'),
    path('api/conversations/<int:conversation_id>/', views.api_delete_conversation, name='api_delete_conversation'),
]