from flask import request, jsonify, Blueprint, abort
from flask_pymongo import ObjectId, MongoClient
from jwt import encode
from datetime import datetime
from hashlib import sha256

connection_str = "mongodb://localhost/"
client = MongoClient(connection_str)
db = client.myBlogApp.user


def hash_str(str):
    return sha256(str.encode()).hexdigest()


user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/new", methods=["POST"])
def new_user():

    # Catching values
    user = request.json["User"]
    password = hash_str(request.json["password"])

    id = db.insert_one(
        {"user": user, "password": password, "date": str(datetime.today())}
    )

    return jsonify({"_id": str(ObjectId(id.inserted_id))})


@user.route("/login", methods=["POST"])
def login():

    # Catching values
    user = request.json["User"]
    password = hash_str(request.json["password"])

    original_user = db.find_one({"user": user})

    if original_user.password != password:
        abort(404)
    else:
        return jsonify(
            {
                "token": encode(
                    {"user": original_user["user"], "date": original_user["date"]},
                    "SECRET PASSWORD",
                )
            }
        )
