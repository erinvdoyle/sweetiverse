const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);

const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#6c757d'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

const card = elements.create('card', { style: style });
card.mount('#card-element');

card.on('change', function (event) {
    const errorDiv = document.getElementById('card-errors');
    if (event.error) {
        errorDiv.textContent = event.error.message;
    } else {
        errorDiv.textContent = '';
    }
});

const form = document.getElementById('payment-form');
const submitButton = document.getElementById('submit-button');
const loadingOverlay = document.getElementById('loading-overlay');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    card.update({ 'disabled': true });
    submitButton.disabled = true;
    if (loadingOverlay) loadingOverlay.classList.remove('d-none');

    const saveInfo = Boolean(document.querySelector('#id-save-info')?.checked);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    const url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: form.full_name.value.trim(),
                    phone: form.phone_number.value.trim(),
                    email: form.email.value.trim(),
                    address: {
                        line1: form.street_address1.value.trim(),
                        line2: form.street_address2.value.trim(),
                        city: form.city.value.trim(),
                        state: form.county.value.trim(),
                        postal_code: form.postcode.value.trim(),
                        country: form.country.value,
                    }
                }
            },
            shipping: {
                name: form.full_name.value.trim(),
                phone: form.phone_number.value.trim(),
                address: {
                    line1: form.street_address1.value.trim(),
                    line2: form.street_address2.value.trim(),
                    city: form.city.value.trim(),
                    state: form.county.value.trim(),
                    postal_code: form.postcode.value.trim(),
                    country: form.country.value,
                }
            },
        }).then(function (result) {
            if (result.error) {
                const errorDiv = document.getElementById('card-errors');
                errorDiv.textContent = result.error.message;

                card.update({ 'disabled': false });
                submitButton.disabled = false;
                if (loadingOverlay) loadingOverlay.classList.add('d-none');
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // Reload page on failure
        location.reload();
    });
});
