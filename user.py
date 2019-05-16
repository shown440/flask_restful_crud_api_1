import sqlite3
import cx_Oracle

from flask_restful import Resource, reqparse

#####################################################
##### Finding User Class ############################
#####################################################
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # ##############################################################
    # ########### SQLite3 DB part ####################################
    # ##############################################################
    @classmethod
    def find_by_username(cls, username):

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2]) #user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user
        
    ##############################################################
    ########### Orace DB part ####################################
    ##############################################################
    # @classmethod
    # def find_by_username(cls, username):
    #
    #     connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM users WHERE username=:username"
    #     result = cursor.execute(query, (username,)) #, (username,)
    #     row = result.fetchone()
    #     if row is not None:
    #         user = cls(row[0], row[1], row[2])
    #     else:
    #         user = None
    #
    #     connection.close()
    #     return user
    #
    # @classmethod
    # def find_by_id(cls, _id):
    #
    #     connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM users WHERE id=:id"
    #     result = cursor.execute(query, (_id,)) #, (_id,)
    #     row = result.fetchone()
    #     if row is not None:
    #         user = cls(row[0], row[1], row[2])
    #     else:
    #         user = None
    #
    #     connection.close()
    #     return user

###############################################################
###### User Register/ Signup Class ############################
###############################################################
class UserRegister(Resource):
    ##############################################################
    ########### Signin to SQLite3 DB part ########################
    ##############################################################
    parser = reqparse.RequestParser()

    parser.add_argument("username",
        type = str,
        required = True,
        help = "User name cannot be blank."
    )
    parser.add_argument("password",
        type = str,
        required = True,
        help = "Password name cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message":"{} is already exist".format(data["username"])}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # int=INTEGER. but if we need auto incremented id then we have to write INTEGER
        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"],))

        connection.commit()
        connection.close()

        return {"message":"{} is created successfully as your authentication user".format(data["username"])}, 201

    ##############################################################
    ########### Signin to Oracle DB part ########################
    ##############################################################
    # parser = reqparse.RequestParser()
    #
    # parser.add_argument("username",
    #     type = str,
    #     required = True,
    #     help = "User name cannot be blank."
    # )
    # parser.add_argument("password",
    #     type = str,
    #     required = True,
    #     help = "Password name cannot be blank."
    # )
    # parser.add_argument("role",
    #     type = str,
    #     required = True,
    #     help = "Role name cannot be blank."
    # )
    #
    # def post(self):
    #     data = UserRegister.parser.parse_args()
    #
    #     if User.find_by_username(data["username"]):
    #         return {"message":"{} is already exist".format(data["username"])}, 400
    #
    #     connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
    #     cursor = connection.cursor()
    #
    #     # int=INTEGER. but if we need auto incremented id then we have to write INTEGER
    #     insert_query = "INSERT INTO users VALUES(:1, :2, :3, :4)"
    #     cursor.execute(insert_query, (None, data["username"], data["password"], data["role"]))
    #
    #     connection.commit()
    #     connection.close()
    #
    #     return {"message":"{} is created successfully as your authentication user".format(data["username"])}, 201
