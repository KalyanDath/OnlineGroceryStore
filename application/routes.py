from flask import Flask, request, render_template, redirect, url_for
from flask import current_app as app
from application.models import User, Role, Category, Products, Cart, Bills, Bill_items
from flask_security import login_required, current_user, roles_required
from werkzeug.utils import secure_filename
import os
import math
from .database import db

@app.route("/")
def home():
    categories = Category.query.all()
    return render_template("index.html",category = categories)

@app.route("/admin/dashboard")
@login_required
@roles_required('admin')
def admin_dashboard():
    categories = Category.query.all()
    return render_template("admin_dashboard.html",categories=categories)


@app.route("/category/create", methods = ["GET","POST"])
@login_required
@roles_required('admin')
def create_category():
    if request.method == "GET":
        return render_template("create_category.html")
    else:
        cat_name = request.form["category_name"]
        if not cat_name.isalnum():
            return render_template("create_category.html",error="yes")
        new_category = Category(category_name = cat_name)

        db.session.add(new_category)  # needs a try catch block here
        db.session.commit()

        return redirect(url_for("admin_dashboard"))


@app.route("/category/get/<cat_name>", methods = ["GET"])
@login_required
@roles_required('admin')
def get_category(cat_name):
    category = Category.query.filter_by(category_name = cat_name).first()
    if not validate(category):
        return render_template("error.html")
    if category is not None:
        return render_template("read_category.html", category = category)
    else:
        return "Hello" ## need some work



@app.route("/category/update/<cat_name>", methods = ["GET","POST"])
@login_required
@roles_required('admin')
def update_category(cat_name):
    category = Category.query.filter_by(category_name = cat_name).first()
    if not validate(category):
        return render_template("error.html")
    if request.method == "GET":
        return render_template("update_category.html", category=category)
    else:
        category_name = request.form["category_name"]
        if not category_name.isalnum():
            return render_template("update_category.html", category=category,error="yes")
        category.category_name = category_name
        db.session.commit()
        return redirect(url_for("admin_dashboard"))



@app.route("/category/delete/<cat_name>", methods = ["GET","POST"])
@login_required
@roles_required('admin')
def delete_category(cat_name):
    category = Category.query.filter_by(category_name = cat_name).first()
    if not validate(category):
        return render_template("error.html")
    if category == None:
        return redirect(url_for("admin_dashboard"))
    if request.method == "GET":
        return render_template("delete_category.html", category=category)
    elif request.method == "POST":
        for product in category.products:
            cart_items = Cart.query.filter_by(product_id = product.product_id).all()
            for item in cart_items:
                db.session.delete(item)
            db.session.delete(product)
        db.session.delete(category)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))
        


@app.route("/product/create/<cat_name>", methods = ["GET","POST"])
@login_required
@roles_required('admin')
def create_product(cat_name):
    category = Category.query.filter_by(category_name = cat_name).first()
    if not validate(category):
        return render_template("error.html")

    if not validate(category):
        return render_template("error.html")

    if request.method == "GET":
        return render_template("create_product.html",category=cat_name)
    else:
        product_name = request.form["product_name"]
        unit = request.form["unit"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        new_product = Products(product_name=product_name, category_id=category.category_id, unit = unit, price = price, quantity = quantity)
        db.session.add(new_product)  # needs a try catch block here
        db.session.commit()

        return redirect(url_for("admin_dashboard"))


@app.route("/product/get/<prod_name>", methods = ["GET"])
@login_required
@roles_required('admin')
def get_product(prod_name):
    product = Products.query.filter_by(product_name = prod_name).first()
    if not validate(product):
        return render_template("error.html")
    if product is not None:
        return render_template("read_product.html", product = product)
    else:
        return "Hello"  ## need some work


@app.route("/product/update/<prod_name>", methods = ["GET","POST"])
@login_required
@roles_required('admin')
def update_product(prod_name):
    product = Products.query.filter_by(product_name=prod_name).first()
    if not validate(product):
        return render_template("error.html")
    if request.method == "GET":
        return render_template("update_product.html",product=product)
    elif request.method == "POST":
        product.product_name = request.form["product_name"]
        product.unit = request.form["unit"]
        product.price = request.form["price"]
        product.quantity = request.form["quantity"]
        db.session.commit()
        return redirect(url_for("admin_dashboard"))


@app.route("/product/delete/<prod_name>", methods = ["GET","POST"])
@login_required
@roles_required('admin')
def delete_product(prod_name):
    product = Products.query.filter_by(product_name=prod_name).first()
    if not validate(product):
        return render_template("error.html")
    if request.method == "GET":
        return render_template("delete_product.html", product=product)
    elif request.method == "POST":
        cart_items = Cart.query.filter_by(product_id = product.product_id).all()
        for item in cart_items:
            db.session.delete(item)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

@app.errorhandler(403)
def not_authorized(e):
    return render_template('error.html'), 403

@app.route("/search", methods = ["POST"])
def search_category():
    if request.method == "POST":
        category_name = request.form["category"]
        category = Category.query.filter_by(category_name = category_name).first()
        if not validate(category):
            return render_template("error.html")
        else:
            products = Products.query.filter_by(category_id = category.category_id).all()
            return render_template('search_results.html', products=products)
        
@app.route("/search_products", methods = ["POST"])
def search_products():
    if request.method == "POST":
        product_name = request.form["product_name"]
        # Some validation required on product_name to be implemented later......

        products = Products.query.filter(Products.product_name.like(f'%{product_name}%')).all()   # This shouldnot have worked!!!
        if products==[]:
            return "No Results"
        else:
            return render_template("search_results.html", products=products)

@app.route("/add_product/<product_name>", methods=["GET","POST"])
@login_required
def add_product(product_name):
    if request.method == "GET":
        product = Products.query.filter_by(product_name=product_name).first()
        if product is None:
            return "Error"
        return render_template("add_product.html", product=product,flag="no")
    if request.method == "POST":
        quantity = request.form["quantity"]   #need to check if quantity is greater than exisiting quantity
        product = Products.query.filter_by(product_name=product_name).first()

        if product is None:
            return "Error"   #Change this to a proper html page
        if int(quantity) > product.quantity:
            return render_template("add_product.html", product=product,flag="quantity")

        existing = Cart.query.filter_by(product_id = product.product_id, user_id= current_user.id).first()
        if existing is not None:
            existing.quantity += int(quantity)
            db.session.commit()
            return render_template("add_product.html", product=product,flag="yes")
        
        price = product.price
        user_id = current_user.id
        cart_item = Cart(user_id=user_id, product_id = product.product_id, quantity=quantity)

        db.session.add(cart_item)  # needs a try catch block here
        db.session.commit()

        return render_template("add_product.html",product=product, flag="yes")

@app.route("/view_cart", methods=["GET"])
@login_required
def view_cart():
    user_id = current_user.id
    cart = Cart.query.filter_by(user_id=user_id).all()
    total_price = 0
    for cart_item in cart:
        total_price += cart_item.quantity * cart_item.product.price

    return render_template("view_cart.html", cart_items=cart, total_price = total_price)

@app.route("/buy_product", methods=["POST"])
@login_required
def buy_product():
    user_id = current_user.id
    cart = Cart.query.filter_by(user_id=user_id).all()
    total_price = 0
    for cart_item in cart:
        total_price += cart_item.quantity * cart_item.product.price
    stock_unavailable=[]

    # Validation with products table with each product in cart...
    total_amount = 0
    for cart_item in cart:
        if cart_item.product.quantity < cart_item.quantity:
            stock_unavailable.append(cart_item.product.product_name)
        else:
            total_amount += cart_item.quantity * cart_item.product.price
    
    if len(stock_unavailable) !=0:
        return render_template("view_cart.html", error_code =1, stock_error = stock_unavailable,cart_items=cart,total_price = total_price )

    new_bill = Bills(user_id = user_id , total_amount = total_amount)
    for cart_item in cart:
        product = Products.query.filter_by(product_id=cart_item.product.product_id).first()
        product.quantity = product.quantity - cart_item.quantity
        item = Bill_items(product_name = cart_item.product.product_name, price =  cart_item.product.price, quantity = cart_item.quantity)
        new_bill.bill_items.append(item)
        db.session.delete(cart_item)

    db.session.add(new_bill)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/review_product/<product_name>", methods=["GET","POST"])
@login_required
def review_product(product_name):
    user_id = current_user.id
    product = Products.query.filter_by(product_name=product_name).first()
    product =  Cart.query.filter_by(user_id = user_id, product_id = product.product_id ).first()
    
    if request.method == "GET":
        return render_template("review_product.html",product=product)
    else:
        
        quantity = request.form["quantity"]   #need to check if quantity is greater than exisiting quantity

        if product is None:
            return "Error: Product is not Found."   #Change this to a proper html page
        if int(quantity) > product.product.quantity:
            return render_template("review_product.html", product=product,flag="quantity")
        
        product.quantity = int(quantity)
        db.session.commit()

        product = Products.query.filter_by(product_name=product_name).first()
        product =  Cart.query.filter_by(user_id = user_id, product_id = product.product_id ).first()

        return render_template("review_product.html",product=product,flag="yes")


@app.route("/delete_cart_product/<product_name>", methods=["GET","POST"])
@login_required
def delete_cart_product(product_name):
    user_id = current_user.id
    product = Products.query.filter_by(product_name=product_name).first()
    product = Cart.query.filter_by(user_id = user_id , product_id = product.product_id).first()
    if request.method == "GET":
        return render_template("delete_cart_product.html",product=product)
    elif request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("view_cart"))

@app.route("/profile", methods=["GET"])
@login_required    
def profile():
    if request.method == "GET":
        bills = Bills.query.filter_by(user_id = current_user.id).all()
        return render_template("profile.html",bills=bills)


def validate(item):
    if item is None:
        return False
    else:
        return True