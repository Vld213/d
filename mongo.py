import pymongo
from config import Auth

mongo = pymongo.MongoClient("mongodb+srv://Vlad:Belluchi2023@cluster0.pbknkxp.mongodb.net/test")
db = mongo.r_new

def set(collection, id, data):
    i = {"_id":id}
    if db[collection].count_documents({"_id":id}) == 0:
        db[collection].insert_one({**i, **data})
    else:
        db[collection].update_one(i, {"$set":data})
