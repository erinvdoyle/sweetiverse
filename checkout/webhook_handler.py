from django.http import HttpResponse

class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Generic event handler."""
        return HttpResponse(content=f'Unhandled webhook received: {event["type"]}', status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle successful payment."""
        return HttpResponse(content='PaymentIntent succeeded webhook received.', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle failed payment."""
        return HttpResponse(content='Webhook received.', status=200)
