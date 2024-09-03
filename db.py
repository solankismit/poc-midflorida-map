
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://projectssmit:8FvTZSs4pQ7sADQK@midfloridadata.nungw.mongodb.net/?retryWrites=true&w=majority&appName=MidFloridaData"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)