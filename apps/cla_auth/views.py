from django.http import HttpResponse
from django.views import View


class DebugView(View):
    def dispatch(self, request, *args, **kwargs):
        headers = ["request headers"]
        print("=== HEADERS ===")

        for key, value in request.headers.items():
            print(f"{key}: {value}")
            headers.append(f"{key}: {value}")

        print("=== META ===")
        headers.append("request META")

        for key, value in request.META.items():
            if key.startswith("HTTP_") or key in (
                "REMOTE_ADDR",
                "SERVER_PORT",
                "SERVER_NAME",
                "wsgi.url_scheme",
            ):
                headers.append(f"{key}: {value}")

                print(f"{key}: {value}")

        return HttpResponse("\n".join(headers))
