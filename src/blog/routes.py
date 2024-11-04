from flask import request, jsonify, Blueprint, abort
from flask_pymongo import ObjectId, MongoClient
from datetime import datetime

connection_str = "mongodb://localhost/"
client = MongoClient(connection_str)
db = client.myBlogApp.blog

blog = Blueprint("blog", __name__, url_prefix="/blog")


# http://localhost:5000/blog/new
@blog.route("/new", methods=["POST"])
def new_blog():

    # Catching values
    tittle = request.json["title"]
    body = request.json["body"]

    id = db.insert_one({"tittle": tittle, "body": body, "date": str(datetime.today())})

    return jsonify({"_id": str(ObjectId(id.inserted_id))})


@blog.route("/get")
def login():

    docs = []

    for doc in db.find():
        docs.append({"title": doc["title"], "body": doc["body"], "date": doc["date"]})

    return jsonify({"blogs": docs})
