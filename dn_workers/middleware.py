from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import WorkerProfile
from django.core.exceptions import ObjectDoesNotExist

class WorkerProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Allow static files
        if request.path.startswith(settings.STATIC_URL):
             return self.get_response(request)
        
        # Check for media url if configured
        if hasattr(settings, 'MEDIA_URL') and settings.MEDIA_URL and settings.MEDIA_URL != '/' and request.path.startswith(settings.MEDIA_URL):
            return self.get_response(request)

        # Allow admin interface
        if request.path.startswith('/admin/'):
             return self.get_response(request)

        # Allow logout
        try:
            logout_url = reverse('account_logout')
            if request.path == logout_url:
                return self.get_response(request)
        except Exception:
            # If reverse fails or route doesn't exist, ignore
            pass

        try:
            # Resolve URLs
            create_profile_url = reverse('create_worker_profile')
            pending_activation_url = reverse('pending_activation')
            
            try:
                # Access related profile
                profile = request.user.worker_profile
                
                # Check activation status
                if not profile.is_active:
                    if request.path != pending_activation_url:
                        return redirect('pending_activation')
                        
            except (WorkerProfile.DoesNotExist, ObjectDoesNotExist, AttributeError):
                # No worker profile found
                if request.path != create_profile_url:
                    return redirect('create_worker_profile')
                    
        except Exception:
            # Fail safely if URLs can't be reversed or other unexpected errors
            pass

        return self.get_response(request)
