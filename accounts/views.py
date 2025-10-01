from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('chat:home')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('chat:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        # Notification removed per user request
        return response


@login_required
def profile_view(request):
    """User profile view with update functionality"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'form': form
    })


@login_required
def remove_profile_picture(request):
    """Remove user's profile picture"""
    if request.method == 'POST':
        user = request.user
        if user.profile_picture:
            # Delete the file from storage
            user.profile_picture.delete(save=False)
            # Clear the field
            user.profile_picture = None
            user.save()
            messages.success(request, 'Profile picture removed successfully!')
        else:
            messages.info(request, 'No profile picture to remove.')
    
    return redirect('accounts:profile')