import stripe
import json
import os
from flask import Flask, render_template, jsonify, request, send_from_directory
from website.home import home
from dotenv import load_dotenv, find_dotenv


@home.route("/")
def initialize():
    return render_template("home/home.html")


# Setup Stripe python client library.
load_dotenv(find_dotenv())

# Ensure environment variables are set.
price = os.getenv('PRICE')
if price is None or price == 'price_12345' or price == '':
    print('You must set a Price ID in .env. Please see the README.')
    exit(0)


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')


@home.route('/', methods=['GET'])
def get_example():
    return render_template('index.html')


@home.route('/config', methods=['GET'])
def get_publishable_key():
    price = stripe.Price.retrieve(os.getenv('PRICE'))
    return jsonify({
      'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
      'unitAmount': price['unit_amount'],
      'currency': price['currency']
    })

# Fetch the Checkout Session to display the JSON result on the success page
@home.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@home.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.data)
    domain_url = os.getenv('DOMAIN')

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url +
            "/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/canceled.html",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price": os.getenv('PRICE'),
                    "quantity": data['quantity']
                }
            ]
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@home.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
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
