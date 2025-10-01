import requests
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)


class AIService:
    """Service class for handling AI interactions with Euron API"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'EURON_API_KEY', None)
        self.api_url = "https://api.euron.one/api/v1/euri/chat/completions"
        self.model = "gpt-4.1-nano"  # Default model
        
        if not self.api_key:
            logger.warning("EURON_API_KEY not found in settings")
    
    def _make_api_request(self, messages):
        """Make a request to the Euron API"""
        if not self.api_key:
            raise Exception("API key not configured")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": messages,
            "model": self.model
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Euron API request failed: {e}")
            raise
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate AI response using Euron API or fallback
        """
        if not self.api_key:
            return self._fallback_response(message)
            
        try:
            # Prepare conversation context
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Be conversational, informative, and friendly."}
            ]
            
            # Add conversation history if provided (last 10 messages for context)
            if conversation_history:
                recent_messages = list(conversation_history.order_by('-created_at')[:10])
                recent_messages.reverse()  # Put them in chronological order
                for msg in recent_messages:
                    role = "user" if msg.is_from_user else "assistant"
                    messages.append({"role": role, "content": msg.content})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Generate response using Euron API
            response_data = self._make_api_request(messages)
            
            # Extract response from API response
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"Unexpected API response format: {response_data}")
                return "I'm sorry, I received an unexpected response format from the AI service."
            
        except Exception as e:
            logger.error(f"Euron API generation failed: {e}")
            return f"I'm sorry, I'm having trouble responding right now. Error: {str(e)}"
    
    def _fallback_response(self, message):
        """Simple fallback responses when Euron API is not available"""
        responses = {
            "hello": "Hello! I'm a simple AI assistant. The Euron API is not configured yet.",
            "hi": "Hi there! I'm here to help, though I'm running in demo mode.",
            "how are you": "I'm doing well, thank you! I'm an AI assistant.",
            "what can you do": "I can have conversations with you. For full AI capabilities, please configure your Euron API key.",
        }
        
        message_lower = message.lower().strip()
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        return f"I received your message: '{message}'. I'm a demo AI assistant. To enable full AI capabilities, please configure your Euron API key in the settings."
    
    def generate_conversation_title(self, first_message):
        """
        Generate a title for the conversation based on the first message
        """
        if not self.api_key:
            return first_message[:30] + ('...' if len(first_message) > 30 else '')
            
        try:
            messages = [
                {"role": "system", "content": "Generate a short, descriptive title (max 5 words) for a conversation that starts with the following message:"},
                {"role": "user", "content": first_message}
            ]
            
            response_data = self._make_api_request(messages)
            
            if 'choices' in response_data and len(response_data['choices']) > 0:
                title = response_data['choices'][0]['message']['content'].strip().replace('"', '')
                return title[:50]  # Ensure it's not too long
            
            # Fallback to truncated message
            return first_message[:30] + ('...' if len(first_message) > 30 else '')
            
        except Exception as e:
            logger.error(f"Title generation failed: {e}")
            # Fallback to truncated message
            return first_message[:30] + ('...' if len(first_message) > 30 else '')