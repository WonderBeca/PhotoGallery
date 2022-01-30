import datetime
from functools import wraps
import uuid
from bson import ObjectId
from flask import session, flash, redirect, url_for
from flask_login import current_user
from model.database import mongo_client
from werkzeug.security import generate_password_hash, check_password_hash


class User():

    def __init__(self, username, email, password, roles, _id=None, must_hash=False):
        
        self._id = ObjectId() if _id is None else _id
        self.username = username
        self.email = email
        self.roles = roles

        self.password = password
        if must_hash:
            self.password = generate_password_hash(self.password)

        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True

    # flask-login required methods
    def get_id(self):
        return str(self._id)

    # My methods?
    @staticmethod
    def get_by_username(username):
        data = mongo_client.get_collection(
            'users').find_one({"username": username})
        if data is not None:
            return User(**data)

    @staticmethod
    def get_by_email(email):
        data = mongo_client.get_collection('users').find_one({"email": email})
        print(data)
        if data is not None:
            return User(**data)

    @staticmethod
    def get_by_id(_id):
        data = mongo_client.get_collection('users').find_one({"_id": ObjectId(_id)})
        if data is not None:
            return User(**data)

    def login_valid(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def register(username, email, password, role):
        user = User.get_by_email(email)
        if user is None:
            new_user = User(username, email, password,
                            roles=role, must_hash=True)
            new_user.save_to_mongo()
            return True
        else:
            return False

    def toggle_login_on(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def toggle_login_off(self):
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True

    def login(self, password: str):
        if self.login_valid(password):
            self.toggle_login_on()

            return True
        else:
            self.toggle_login_off()

            return False

    def json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "roles": self.roles
        }

    def save_to_mongo(self):
        mongo_client.get_collection('users').insert_one(self.json())


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.roles and "admin" in current_user.roles:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('home_page'))

    return wrap
