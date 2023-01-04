from unicodedata import category
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import product_model

class Category:
    def __init__(self,data):
        self.categoryId = data['categoryId']
        self.name = data['name']
        self.products = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM categories;"
        results = connectToMySQL('python_project_schema').query_db(query)
        all_categories = []
        for row in results:
            all_categories.append(cls(row))
        return all_categories
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM categories LEFT JOIN products ON categories.categoryId = products.category_id WHERE categoryId = %(categoryId)s;"
        results = connectToMySQL('python_project_schema').query_db(query,data)
        if len(results) > 0:
            category = cls(results[0])
            if results[0]['productId'] == None:
                return category
            for row in results:
                data = {
                    **row,
                    'name' : row['products.name']
                }
                category.products.append(product_model.Product(data))
            return category
        return False