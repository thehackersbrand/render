from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    """Model to store chat conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Only try to set title if the conversation already exists (has a primary key)
        if not self.title and self.pk and self.messages.exists():
            # Set title to first user message (truncated)
            first_message = self.messages.filter(is_from_user=True).first()
            if first_message:
                self.title = first_message.content[:50] + ('...' if len(first_message.content) > 50 else '')
        super().save(*args, **kwargs)


class Message(models.Model):
    """Model to store individual messages in conversations"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_from_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        sender = "User" if self.is_from_user else "AI"
        return f"{sender}: {self.content[:50]}..."