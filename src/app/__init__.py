from flask import Flask
from flask_cors import CORS

from user.routes import user
from blog.routes import blog


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(user)
    app.register_blueprint(blog)

    return app