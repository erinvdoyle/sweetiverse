from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """ Error Handler 500 - Internal Server Error """
    return render(request, "errors/500.html", status=500)


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = "account/email/email_confirmation.html"

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()

        if not confirmation.email_address.verified:
            confirmation.confirm(self.request)

        return super().get(*args, **kwargs)
