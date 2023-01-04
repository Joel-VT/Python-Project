from flask_app import app
from flask import request, render_template, redirect, flash, session, jsonify
from flask_app.models.product_model import Product
from flask_app.models.category_model import Category
from flask_app.models.user_model import User
# import json
# import os
# import stripe
# stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route("/show/<int:id>/category")
def show_category(id):
    if not 'user_id' in session:
        return redirect('/')
    return render_template("category_show.html", category = Category.get_one({'categoryId': id}), user = User.get_by_id({'id' : session['user_id']}))

@app.route("/view/product/<int:id>")
def view_product(id):
    if not 'user_id' in session:
        return redirect('/')
    return render_template("view_product.html", user = User.get_by_id({'id' : session['user_id']}), product = Product.get_one({'productId': id}))

@app.route("/add/<int:id>/cart")
def add_to_cart(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'product_id': id
    }
    Product.add_kart(data)
    return redirect(f"/view/product/{id}")

@app.route("/view/cart")
def cart():
    if not 'user_id' in session:
        return redirect('/')
    user = User.get_by_id({'id' : session['user_id']})
    subtotal = 0
    for product in user.kart:
        subtotal += product.price
    data = {
    'tax': round((float(subtotal) * 0.09), 2),
    'subtotal': float(subtotal),
    'total': float(subtotal) + (float(subtotal) * 0.09)
    }
    return render_template("view_kart.html", user = user, data = data)

@app.route("/remove/item/<int:id>")
def remove_item_from_kart(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'product_id': id
    }
    Product.remove_from_kart(data)
    return redirect("/view/cart")

# @app.route("/render/payment")
# def render_payment_form():
#     return render_template("checkout.html")

# @app.route('/get/kart')
# def get_kart_items():
#     data = {
#         'id': session['user_id']
#     }
#     # jsonify will serialize data into JSON format.
#     return jsonify(User.get_kart(data))

# @app.route('/create-payment-intent', methods=['POST'])
# def create_payment():
#     try:
#         data = json.loads(request.data)
#         # Create a PaymentIntent with the order amount and currency
#         intent = stripe.PaymentIntent.create(
#             amount=Product.calculate_order_amount(data['items']),
#             currency='usd',
#             automatic_payment_methods={
#                 'enabled': True,
#             },
#         )
#         return jsonify({
#             'clientSecret': intent['client_secret']
#         })
#     except Exception as e:
#         return jsonify(error=str(e)), 403
