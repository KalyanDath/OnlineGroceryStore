from flask_restful import Resource, Api,fields,marshal_with, reqparse
from flask import current_app as app
from application.database import db
from flask import jsonify
from application.models import Category, Products, Cart
import werkzeug
from application.validation import CategoryNotFoundError, ValidationError, CategoryExistsError, ProductNotFoundError,  ProductExistsError

resource_fields = {
    'category_id' : fields.Integer,
    'category_name' : fields.String,
}
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("category_name")

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument("category_name")



class CategoryAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, category_id):
        category = Category.query.filter_by(category_id = category_id).first()

        if category is not None:
            return category
        else:
           raise CategoryNotFoundError

    @marshal_with(resource_fields)
    def put(self,category_id):
        category = Category.query.filter_by(category_id = category_id).first()

        if category is not None:
            args = update_user_parser.parse_args()
            category_name = args.get("category_name",None)


            if category_name is None:
                raise ValidationError(status_code = 400, error_code = "C001", error_message="Category Name is required")
            category.category_name = category_name
            db.session.commit()
            return category
        else:
            raise CategoryNotFoundError
        
    def delete(self,category_id):
        category = Category.query.filter(Category.category_id == category_id).first()
        if category is None:
            raise CategoryNotFoundError
        else:
            for product in category.products:
                db.session.delete(product)
            db.session.delete(category)
            db.session.commit()
            return "", None
        
    @marshal_with(resource_fields)    
    def post(self):
        args = create_user_parser.parse_args()
        category_name = args.get("category_name",None)
        if category_name is None:
                raise ValidationError(status_code = 400, error_code = "C001", error_message="Category Name is required")
        category = Category.query.filter(Category.category_name == category_name).first()
        if category is not None:
            raise CategoryExistsError
        
        new_category = Category(category_name = category_name)
        db.session.add(new_category)
        db.session.commit()

        return new_category

resource_fields_p = {
    'product_id' : fields.Integer,
    'product_name' : fields.String,
    'category_id'  : fields.Integer,
    'price' : fields.Float,
    'unit' :  fields.String,
    'quantity' : fields.Integer
}
create_product_parser = reqparse.RequestParser()
create_product_parser.add_argument("product_name")
create_product_parser.add_argument("category_id")
create_product_parser.add_argument("price")
create_product_parser.add_argument("unit")
create_product_parser.add_argument("quantity")

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument("product_name")
update_product_parser.add_argument("category_id")
update_product_parser.add_argument("price")
update_product_parser.add_argument("unit")
update_product_parser.add_argument("quantity")

class ProductAPI(Resource):
    @marshal_with(resource_fields_p)
    def get(self, product_id):
        product = Products.query.filter_by(product_id = product_id).first()

        if product is not None:
            return product
        else:
           raise ProductNotFoundError
    @marshal_with(resource_fields_p)   
    def put(self,product_id):
        product = Products.query.filter_by(product_id = product_id).first()
        if product is not None:
            args = update_product_parser.parse_args()
            product_name = args.get("product_name",None)
            category_id = args.get("category_id", None)
            price = args.get("price",None)
            unit = args.get("unit",None)
            quantity = args.get("quantity",None)

            if product_name is None:
                raise ValidationError(status_code = 400, error_code="P01", error_message='Product Name is required')
            
            if category_id is not None:
                category = Category.query.filter(Category.category_id == category_id).first()
                if category is None:
                    raise ValidationError(status_code=400, error_code="P02", error_message='Category ID does not exist.')
            
            try:
                if price is not None:
                    p = float(price)   
            except:
                raise ValidationError(status_code = 400, error_code="P03", error_message='Price should be a number.')
            
            if unit is not None and unit not in ["unit","kg","litres","dozen"]:
                raise ValidationError(status_code = 400, error_code="P04", error_message="Invalid unit value. Must be 'unit', 'kg','litres', or 'dozen'.")
        
            try:
                if quantity is not None:
                    c = int(quantity)
            except:
                raise ValidationError(status_code = 400, error_code="P05", error_message='Quantity should be a integer.')
            
            if quantity is not None:
                if int(quantity) < 0 :
                    raise ValidationError(status_code = 400, error_code="P06", error_message='Quantity should be atleast 1.')
                
            product.product_name  = product_name
            if category_id is not None:
                product.category_id = category_id
            if price is not None:
                product.price = price
            if unit is not None:
                product.unit = unit
            if quantity is not None:
                product.quantity = quantity
            db.session.commit()
            return product
        else:
           raise ProductNotFoundError
        
    def delete(self,product_id):
        product = Products.query.filter(Products.product_id == product_id).first()
        if product is None:
            raise ProductNotFoundError
        else:
            cart_items = Cart.query.filter_by(product_id = product.product_id).all()
            for item in cart_items:
                db.session.delete(item)
            db.session.delete(product)
            db.session.commit()
            return "Product Deleted", None
        
    @marshal_with(resource_fields_p)    
    def post(self):
        args = create_product_parser.parse_args()
        product_name = args.get("product_name",None)
        category_id = args.get("category_id", None)
        price = args.get("price",None)
        unit = args.get("unit",None)
        quantity = args.get("quantity",None)

        if product_name is None:
            raise ValidationError(status_code = 400, error_code="P01", error_message='Product Name is required')
        if category_id is None:
            raise ValidationError(status_code = 400, error_code="P07", error_message='Category_id is required')
        if price is None:
            raise ValidationError(status_code = 400, error_code="P08", error_message='Price is required')
        if unit is None:
            raise ValidationError(status_code = 400, error_code="P09", error_message='Unit is required')
        if quantity is None:
            raise ValidationError(status_code = 400, error_code="P10", error_message='Quantity is required')

        product = Products.query.filter(Products.product_name == product_name).first()
        if product is not None:
            raise ProductExistsError
        
        category = Category.query.filter(Category.category_id == category_id).first()
        if category is None:
            raise ValidationError(status_code=400, error_code="P02", error_message='Category ID does not exist.')
        
        try:
            p = float(price)   
        except:
            raise ValidationError(status_code = 400, error_code="P03", error_message='Price should be a number.')
        
        if unit not in ["unit","kg","litres","dozen"]:
                raise ValidationError(status_code = 400, error_code="P04", error_message="Invalid unit value. Must be 'unit', 'kg','litres', or 'dozen'.")
        try:
            c = int(quantity)
        except:
            raise ValidationError(status_code = 400, error_code="P05", error_message='Quantity should be a integer.')
        
        if int(quantity) <=0 :
            raise ValidationError(status_code = 400, error_code="P06", error_message='Quantity should be atleast 1.')        
        
        new_product = Products(product_name = product_name, category_id = category_id, price = price, unit = unit, quantity = quantity)
        db.session.add(new_product)
        db.session.commit()

        return new_product
    
class CategoryProductAPI(Resource):

    def get(self,category_id):
        category = Category.query.filter_by(category_id = category_id).first()
        if category is None:
            raise CategoryNotFoundError
        else:
            products =[]
            for product in category.products:
                product_info = {

                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "category_id": product.category_id,
                    "price": product.price,
                    "unit": product.unit,
                    "quantity": product.quantity
                }
                products.append(product_info)
            
        return jsonify(products)