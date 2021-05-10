import json
import os

from config import Development
from website.payment import test_payment

import stripe
from flask import Flask, render_template, render_template_string, jsonify, request, send_from_directory
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
stripe.api_version = os.getenv('STRIPE_API_VERSION')
stripe.api_key = Development.test_stripe_keys['secret_key']


@test_payment.route("/success")
def success():
    return render_template("payment/success.html")


@test_payment.route("/cancelled")
def cancelled():
    return render_template("payment/cancelled.html")


@test_payment.route('/config', methods=['GET'])
def get_publishable_key():
    price = stripe.Price.retrieve(os.getenv('TEST_SMALL_SHIRT_PRICE'))
    return jsonify({
        'publicKey': os.getenv('TEST_STRIPE_PUBLISHABLE_KEY'),
        'unitAmount': price['unit_amount'],
        'currency': price['currency']
    })


# Fetch the Checkout Session to display the JSON result on the success page
@test_payment.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@test_payment.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.data)
    if data['size'] == '1':
        size = os.getenv('TEST_SMALL_SHIRT_PRICE')
    elif data['size'] == '2':
        size = os.getenv('TEST_MEDIUM_SHIRT_PRICE')
    elif data['size'] == '3':
        size = os.getenv('TEST_LARGE_SHIRT_PRICE')
    domain_url = "https://www.treesfromspace.com/"
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
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
                    'price': os.getenv('TEST_SHIPPING_PRICE'),
                    'quantity': 1,
                },
            ],
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@test_payment.route('/test_webhook', methods=['POST'])
def webhook_received():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, Development.test_stripe_keys["TEST_STRIPE_ENDPOINT_SECRET"]
        )
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400
    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        # TODO: run some custom code here
    return "Success", 200
