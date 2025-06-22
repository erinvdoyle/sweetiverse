from django.shortcuts import render
from allauth.account.views import ConfirmEmailView


def index(request):
    return render(request, 'index.html')


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """ Error Handler 500 - Internal Server Error """
    return render(request, "errors/500.html", status=500)


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = "account/email_confirm.html"
