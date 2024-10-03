from .database import db
from flask_security import UserMixin, RoleMixin

class RoleUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))

class Role(db.Model, RoleMixin):
    __tablename__="role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__="user"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship("Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic"))

class Category(db.Model):
    __tablename__= "category"
    category_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    category_name = db.Column(db.Integer())
    products = db.relationship('Products' , backref="category")

class Products(db.Model):
    __tablename__  = 'products'
    product_id = db.Column(db.Integer(), primary_key= True)
    product_name = db.Column(db.String, nullable= False, unique= True)
    category_id = db.Column(db.Integer(), db.ForeignKey("category.category_id"))
    price = db.Column(db.Float, db.CheckConstraint('price >= 0.0', name='check_rate_per_unit'), nullable= False)
    unit = db.Column(db.String,nullable=False, default='unit')    # need to set up some default values.
    quantity = db.Column(db.Integer,db.CheckConstraint('quantity >= 0', name='check_stock_quantity') , nullable= False)   #maybe change to have default value as 0.
   

class Cart(db.Model):
    __tablename__ = "cart"
    user_id = db.Column(db.Integer(),db.ForeignKey("user.id") ,primary_key = True)
    product_id = db.Column(db.Integer(), db.ForeignKey("products.product_id"),primary_key = True)
    quantity = db.Column(db.Integer,db.CheckConstraint('quantity >= 0', name='check_cart_quantity') , nullable= False)
    product = db.relationship("Products", backref="cart")   


class Bills(db.Model):
    __tablename__ = "bills"
    bill_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    #product__id
    total_amount = db.Column(db.Float(), nullable= False)
    bill_items = db.relationship("Bill_items", backref="bills")

class Bill_items(db.Model): #given product_name and price to avoid integrity constriants on deleting a product on products table
    __tablename__ = "bill_items"
    bill_item_id = db.Column(db.Integer(),primary_key = True, autoincrement = True)
    bill_id = db.Column(db.Integer(),db.ForeignKey("bills.bill_id"))
    product_name = db.Column(db.String, nullable= False)
    price = db.Column(db.Float(),db.CheckConstraint('price >= 0.0', name='check_cart_price '), nullable= False)  
    quantity = db.Column(db.Integer,db.CheckConstraint('quantity >= 0', name='check_cart_quantity') , nullable= False)
