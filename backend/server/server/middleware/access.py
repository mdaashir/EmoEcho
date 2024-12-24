from django.http import HttpResponseForbidden

class BlockNonApiUrls:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow the home page ("/") and any path starting with "/api/"
        if request.path == "/" or request.path.startswith("/api/"):
            response = self.get_response(request)
            return response

        # Block all other paths
        return HttpResponseForbidden("Access to this URL is forbidden.")
