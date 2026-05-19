from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class PortLoginRedirectMiddleware(MiddlewareMixin):
    """Redirect requests to the login page when the incoming port matches
    `settings.LOGIN_PORT` and the user is not authenticated.

    Exempts static/media/admin and the login/logout/register paths to avoid
    redirect loops.
    """

    def process_request(self, request):
        login_port = getattr(settings, 'LOGIN_PORT', None)
        if not login_port:
            return None

        try:
            port = int(request.get_port())
        except Exception:
            return None

        # Build a list of exempt path prefixes
        exempt_prefixes = []
        try:
            exempt_prefixes.extend([
                reverse('login'),
                reverse('logout'),
                reverse('register'),
            ])
        except Exception:
            # If reversing fails, ignore named routes
            pass

        # add common static/media/admin prefixes
        exempt_prefixes.extend([
            getattr(settings, 'STATIC_URL', '/static/'),
            getattr(settings, 'MEDIA_URL', '/media/'),
            '/admin/',
        ])

        path = request.path
        for prefix in exempt_prefixes:
            if prefix and path.startswith(prefix):
                return None

        if port == int(login_port) and not request.user.is_authenticated:
            try:
                return redirect(reverse('login'))
            except Exception:
                return redirect('/login/')

        return None
