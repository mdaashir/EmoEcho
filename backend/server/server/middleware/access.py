from django.http import HttpResponseForbidden

class BlockNonApiUrls:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return HttpResponseForbidden("Access to this URL is forbidden.")
        response = self.get_response(request)
        return response
