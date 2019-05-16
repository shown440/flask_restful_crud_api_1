import sqlite3
import cx_Oracle

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

###############################################################################
###############################################################################
##### SQLite3 DB Item(Resource) ###############################################
###############################################################################
###############################################################################

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="Field can't be empty..."
    )

    #@jwt_required()
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # int=INTEGER. but if we need auto incremented id then we have to write INTEGER
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()
        if row:
            return {"item":{"name":row[0], "price":row[1]}}, 200

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message":"{} is not found".format(name)}, 404

    #@jwt_required()
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query="INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item["name"], item["price"], ))

        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"Message":"{} is exist. No need to create it again.".format(name)}, 400

        data = Item.parser.parse_args()
        #print("####################", data)
        item = {"name":name, "price":data["price"]}

        try:
            self.insert(item)
        except:
            return {"message":"{} insertion failed.".format(name)}, 500
        return item, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query="DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()

        return {"message" : "Item {} deleted successfully".format(name)}

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query="UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"], ))

        connection.commit()
        connection.close()

    def put(self, name):

        data = Item.parser.parse_args()

        item_exist = self.find_by_name(name)
        update_item = {"name":name, "price":data["price"]}
        if item_exist is None: # is None
            try:
                self.insert(update_item)
            except:
                return {"message":"Updating error. Please see the update and put method."}, 500
        else:
            try:
                self.update(update_item)
            except:
                return {"message":"Updating error. Please see the update and put method."}, 500
        return update_item

class ItemList(Resource):
    #@jwt_required()
    def get(self):
        items = []

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query="SELECT * FROM items"
        result = cursor.execute(query)

        for row in result:
            items.append({"name":row[0], "price":row[1]})

        connection.close()
        return {"items" : items}

#################################################################################
#################################################################################
##### ORACLE DB Item(Resource) ##################################################
#################################################################################
################################################################################

# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument("price",
#         type=float,
#         required=True,
#         help="Field can't be empty..."
#     )
#
#     @classmethod
#     def find_by_name(cls, name):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         # int=INTEGER. but if we need auto incremented id then we have to write INTEGER
#         query = "SELECT * FROM REST_ITEMS WHERE name=:name"
#         result = cursor.execute(query, (name,))
#         row = result.fetchone()
#
#         connection.close()
#         if row:
#             return {"item":{"name":row[0], "price":row[1]}}, 200
#
#     @jwt_required()
#     def get(self, name):
#         item = self.find_by_name(name)
#         if item:
#             return item
#         return {"message":"{} is not found".format(name)}, 404
#
#     @classmethod
#     def insert(cls, item):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         query="INSERT INTO REST_ITEMS VALUES(:1, :2)"
#         cursor.execute(query, (item["name"], item["price"], ))
#
#         connection.commit()
#         connection.close()
#
#     def post(self, name):
#         if self.find_by_name(name):
#             return {"Message":"{} is exist. No need to create it again.".format(name)}, 400
#
#         data = Item.parser.parse_args()
#         item = {"name":name, "price":data["price"]}
#
#         try:
#             self.insert(item)
#         except:
#             return {"message":"{} insertion failed.".format(name)}, 500
#         return item, 201
#
#
#     def delete(self, name):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         query="DELETE FROM REST_ITEMS WHERE name=:name"
#         cursor.execute(query, (name, ))
#
#         connection.commit()
#         connection.close()
#         return {"message" : "Item {} deleted successfully".format(name)}
#
#     @classmethod
#     def update(cls, item):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         query="UPDATE REST_ITEMS SET price=:1 WHERE name=:2"
#         cursor.execute(query, (item["price"], item["name"], ))
#
#         connection.commit()
#         connection.close()
#
#     def put(self, name):
#         data = Item.parser.parse_args()
#
#         item_exist = self.find_by_name(name)
#         update_item = {"name":name, "price":data["price"]}
#         if item_exist is None: # is None
#             try:
#                 self.insert(update_item)
#             except:
#                 return {"message":"Updating error. Please see the update and put method."}, 500
#         else:
#             try:
#                 self.update(update_item)
#             except:
#                 return {"message":"Updating error. Please see the update and put method."}, 500
#         return update_item
#
# class ItemList(Resource):
#     #@jwt_required()
#     def get(self):
#         items = []
#
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#         query="SELECT * FROM REST_ITEMS"
#         result = cursor.execute(query)
#
#         for row in result:
#             items.append({"name":row[0], "price":row[1]})
#
#         connection.close()
#         return {"items" : items}
