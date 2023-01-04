from flask_app.models import product_model
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.address1 = data['address1']
        self.address2 = data['address2']
        self.zipcode = data['zipcode']
        self.city = data['city']
        self.state = data['state']
        self.country = data['country']
        self.phone = data['phone']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.kart = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('python_project_schema').query_db(query)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def get_kart(cls,data):
        query = "SELECT products.name, products.price FROM users LEFT JOIN kart ON users.id = kart.user_id LEFT JOIN products ON kart.product_id = products.productId WHERE users.id = %(id)s;"
        results = connectToMySQL('python_project_schema').query_db(query,data)
        return results

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN kart ON users.id = kart.user_id LEFT JOIN products ON kart.product_id = products.productId WHERE users.id = %(id)s;"
        results = connectToMySQL('python_project_schema').query_db(query,data)
        if len(results) > 0:
            user = cls(results[0])
            if results[0]['productId'] == None:
                return user
            for row in results:
                user.kart.append(product_model.Product(row))
            return user
        return False

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('python_project_schema').query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,address1,address2,zipcode,city,state,country,phone) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(address1)s,%(address2)s,%(zipcode)s,%(city)s,%(state)s,%(country)s,%(phone)s);"
        return connectToMySQL('python_project_schema').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, address1 = %(address1)s, address2 = %(address2)s, zipcode = %(zipcode)s, city = %(city)s, state = %(state)s, country = %(country)s, phone = %(phone)s WHERE id = %(id)s;"
        return connectToMySQL('python_project_schema').query_db(query,data)
    
    @classmethod
    def update_password(cls,data):
        query = "UPDATE users SET password = %(password)s WHERE id = %(id)s;"
        return connectToMySQL('python_project_schema').query_db(query,data)
    
    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash('*First name required', 'first')
            is_valid = False
        elif len(data['first_name']) < 3:
            flash('*First name has to be at least 2 characters', 'first')
            is_valid = False
        elif not data['first_name'].isalpha():
            flash('*First name should comprise of alphabets only', 'first')
            is_valid = False
        if len(data['last_name']) < 1:
            flash('*Last name required', 'last')
            is_valid = False
        elif len(data['last_name']) < 3:
            flash('*Last name has to be at least 2 characters', 'last')
            is_valid = False
        elif not data['last_name'].isalpha():
            flash('*Last name should comprise of alphabets only', 'last')
            is_valid = False
        if len(data['email']) < 1:
            is_valid = False
            flash('*Email Required', 'email')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('*Invalid Email', 'email')
        if len(data['password']) < 1:
            flash('*Password required', 'pass')
            is_valid = False
        elif len(data['password']) < 8:
            flash('*Password has to be at least 8 characters', 'pass')
            is_valid = False
        elif not any(ele.isupper() for ele in data['password']):
            flash('*Password must contain atleast one upper case', 'pass')
            is_valid = False
        elif not any(ele.isnumeric() for ele in data['password']):
            flash('*Password must contain atleast one number', 'pass')
            is_valid = False
        if len(data['confirm_password']) < 1:
            flash('*Confirm Password', 'confirm')
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash('*Paswords dont match', 'confirm')
            is_valid = False
        if len(data['address1']) < 1:
            flash('*Address1 required', 'address1')
            is_valid = False
        elif len(data['address1']) < 3:
            flash('*Please enter a valid address', 'address1')
            is_valid = False
        if len(data['address2']) < 1:
            flash('*Address2 required', 'address2')
            is_valid = False
        elif len(data['address2']) < 3:
            flash('*Please enter a valid address', 'address2')
            is_valid = False
        if len(data['zipcode']) < 1:
            flash('*Zipcode required', 'zipcode')
            is_valid = False
        elif len(data['zipcode']) < 5 or len(data['zipcode']) > 5:
            flash('*Please enter a valid zipcode', 'zipcode')
            is_valid = False
        if len(data['city']) < 1:
            flash('*City required', 'city')
            is_valid = False
        elif len(data['city']) < 3:
            flash('*Please enter a valid city name', 'city')
            is_valid = False
        if len(data['state']) < 1:
            flash('*State required', 'state')
            is_valid = False
        elif len(data['state']) < 2:
            flash('*Please enter a valid State', 'state')
            is_valid = False
        if len(data['country']) < 1:
            flash('*Country required', 'country')
            is_valid = False
        elif len(data['country']) < 2:
            flash('*Please enter a valid Country', 'country')
            is_valid = False
        if len(data['phone']) < 1:
            flash('*Phone Number required', 'phone')
            is_valid = False
        elif len(data['phone']) < 10 or len(data['phone']) > 10:
            flash('*Please enter a valid phone number', 'phone')
            is_valid = False
        return is_valid

    @staticmethod
    def edit_validator(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash('*First name required', 'first')
            is_valid = False
        elif len(data['first_name']) < 3:
            flash('*First name has to be at least 2 characters', 'first')
            is_valid = False
        elif not data['first_name'].isalpha():
            flash('*First name should comprise of alphabets only', 'first')
            is_valid = False
        if len(data['last_name']) < 1:
            flash('*Last name required', 'last')
            is_valid = False
        elif len(data['last_name']) < 3:
            flash('*Last name has to be at least 2 characters', 'last')
            is_valid = False
        elif not data['last_name'].isalpha():
            flash('*Last name should comprise of alphabets only', 'last')
            is_valid = False
        if len(data['email']) < 1:
            is_valid = False
            flash('*Email Required', 'email')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('*Invalid Email', 'email')
        if len(data['address1']) < 1:
            flash('*Address1 required', 'address1')
            is_valid = False
        elif len(data['address1']) < 3:
            flash('*Please enter a valid address', 'address1')
            is_valid = False
        if len(data['address2']) < 1:
            flash('*Address2 required', 'address2')
            is_valid = False
        elif len(data['address2']) < 3:
            flash('*Please enter a valid address', 'address2')
            is_valid = False
        if len(data['zipcode']) < 1:
            flash('*Zipcode required', 'zipcode')
            is_valid = False
        elif len(data['zipcode']) < 5 or len(data['zipcode']) > 5:
            flash('*Please enter a valid zipcode', 'zipcode')
            is_valid = False
        if len(data['city']) < 1:
            flash('*City required', 'city')
            is_valid = False
        elif len(data['city']) < 3:
            flash('*Please enter a valid city name', 'city')
            is_valid = False
        if len(data['state']) < 1:
            flash('*State required', 'state')
            is_valid = False
        elif len(data['state']) < 2:
            flash('*Please enter a valid State', 'state')
            is_valid = False
        if len(data['country']) < 1:
            flash('*Country required', 'country')
            is_valid = False
        elif len(data['country']) < 2:
            flash('*Please enter a valid Country', 'country')
            is_valid = False
        if len(data['phone']) < 1:
            flash('*Phone Number required', 'phone')
            is_valid = False
        elif len(data['phone']) < 10 or len(data['phone']) > 10:
            flash('*Please enter a valid phone number', 'phone')
            is_valid = False
        return is_valid
    

    @staticmethod
    def password_validator(data):
        is_valid = True
        if len(data['password']) < 1:
            flash('*Password required', 'pass')
            is_valid = False
        elif len(data['password']) < 8:
            flash('*Password has to be at least 8 characters', 'pass')
            is_valid = False
        elif not any(ele.isupper() for ele in data['password']):
            flash('*Password must contain atleast one upper case', 'pass')
            is_valid = False
        elif not any(ele.isnumeric() for ele in data['password']):
            flash('*Password must contain atleast one number', 'pass')
            is_valid = False
        if len(data['confirm_password']) < 1:
            flash('*Confirm Password', 'confirm')
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash('*Paswords dont match', 'confirm')
            is_valid = False
        return is_valid
