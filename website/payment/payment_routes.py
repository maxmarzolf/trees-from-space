from website.payment import payment
from config import stripe_keys
from flask import jsonify, render_template, request
import stripe
import json


@payment.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@payment.route('/secret')
def secret():
    intent = stripe.PaymentIntent.create(
        amount=1099,
        currency='usd',
        metadata={'integration_check': 'accept_a_payment'})
    return jsonify(client_secret=intent.client_secret)










@payment.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


@payment.route("/payment")
def land_here():
    return render_template('payment/payment.html')


@payment.route("/success")
def success():
    return render_template("payment/success.html")


@payment.route("/cancelled")
def cancelled():
    return render_template("payment/cancelled.html")


@payment.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
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
