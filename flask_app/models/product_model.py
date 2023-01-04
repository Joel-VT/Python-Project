from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Product:
    def __init__(self, data):
        self.productId = data['productId']
        self.name = data['name']
        self.price = data['price']
        self.description = data['description']
        self.image = data['image']
        self.stock = data['stock']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.category_id = data['category_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM products;"
        results = connectToMySQL('python_project_schema').query_db(query)
        all_products = []
        for row in results:
            all_products.append(cls(row))
        return all_products

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM products WHERE productID = %(productId)s;"
        result = connectToMySQL('python_project_schema').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])

    @classmethod
    def create(cls, data):
        query = "INSERT INTO products (name,price,description,image,stock,category_id) VALUES(%(name)s,%(price)s,%(description)s,%(image)s,%(stock)s,%(category_id)s);"
        return connectToMySQL('python_project_schema').query_db(query, data)

    @classmethod
    def update_stock(cls, data):
        query = "UPDATE products SET stock = %(stock)s WHERE productId = %(productID)s;"
        return connectToMySQL('python_project_schema').query_db(query, data)

    @classmethod
    def add_kart(cls, data):
        query = "INSERT INTO kart (user_id, product_id) VALUES (%(user_id)s, %(product_id)s);"
        return connectToMySQL('python_project_schema').query_db(query, data)

    @classmethod
    def remove_from_kart(cls, data):
        query = "DELETE FROM kart WHERE user_id = %(user_id)s AND product_id = %(product_id)s;"
        return connectToMySQL('python_project_schema').query_db(query, data)

    @staticmethod
    def validator(data):
        is_valid = True
        return is_valid

    @staticmethod
    def calculate_order_amount(items):
        total = 0
        for product in items:
            total += product['price']
        return total