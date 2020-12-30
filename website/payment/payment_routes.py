import stripe
import json
import os
from website.payment import payment
from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library.
load_dotenv(find_dotenv())
# Ensure environment variables are set.
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]


@payment.route('/config', methods=['GET'])
def get_publishable_key():
    price = stripe.Price.retrieve(os.getenv('SMALL_SHIRT_PRICE'))
    return jsonify({
        'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
        'unitAmount': price['unit_amount'],
        'currency': price['currency']
    })


# Fetch the Checkout Session to display the JSON result on the success page
@payment.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@payment.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.data)
    if data['size'] == '1':
        size = os.getenv('SMALL_SHIRT_PRICE')
    elif data['size'] == '2':
        size = os.getenv('MEDIUM_SHIRT_PRICE')
    elif data['size'] == '3':
        size = os.getenv('LARGE_SHIRT_PRICE')

    domain_url = "https://www.treesfromspace.com"
    stripe.api_key = stripe_keys["secret_key"]
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/",
            payment_method_types=["card"],
            billing_address_collection='required',
            # customer_email='required',
            mode="payment",
            line_items=[
                {
                    'price': size,
                    'quantity': data['quantity'],
                },
                {
                    'price': os.getenv('SHIPPING_PRICE'),
                    'quantity': 1,
                },
            ],
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@payment.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = os.getenv('STRIPE_ENDPOINT_SECRET')
    request_data = json.loads(request.data)
    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']
    print('event ' + event_type)
    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
    return jsonify({'status': 'success'})
