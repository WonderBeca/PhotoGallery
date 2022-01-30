import pymongo

MONGO_URI = "mongodb+srv://rebecaaaaa:TPUGSnMYEbHfzhN3@cluster0.ojots.mongodb.net"

mongo_client = pymongo.MongoClient(
    MONGO_URI, connect=False).get_database('gallery_test')
