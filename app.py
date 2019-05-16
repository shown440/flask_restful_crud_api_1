from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, "/item/<string:name>") ### http://127.0.0.1:5000/student/Shifullah
api.add_resource(ItemList, "/items/")
api.add_resource(UserRegister, "/register/")


if __name__ == '__main__':
    app.debug=True
    app.run()
