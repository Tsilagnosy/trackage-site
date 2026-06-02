from .models import VisitorAnalytics


class VisitorAnalyticsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        excluded_paths = [
            '/admin',
            '/static',
            '/media'
        ]

        if not any(
            request.path.startswith(path)
            for path in excluded_paths
        ):

            ip = self.get_client_ip(request)

            user_agent = request.META.get(
                'HTTP_USER_AGENT',
                ''
            )

            VisitorAnalytics.objects.create(
                ip_address=ip,
                path_visited=request.path,
                browser=user_agent[:255],
                device=user_agent[:255]
            )

        return response

    def get_client_ip(self, request):

        x_forwarded_for = request.META.get(
            'HTTP_X_FORWARDED_FOR'
        )

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip	
	
	
	
	
	
	
	
	
	