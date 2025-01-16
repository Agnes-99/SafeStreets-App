from flask import Flask
import os
from .routes import auth 

def create_app ():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config["DATABASE"] = "safestreets.db"
    app.config["UPLOAD_FOLDER"] ="../static/uploads"
    app.config["ALLOWED_EXTENSIONS"] = {'png','jpg','jpeg','gif','mp4','avi','mov','ogg','wav','mp3'}
    app.secret_key ="Apples&Bananas"

    from .routes import auth
    app.register_blueprint(auth)

    #initialize database 
    from app.db import create_connection, create_tables, close_connection

    def init_db():
        conn = create_connection(app.config["DATABASE"])
        if conn:
            create_tables(conn)
            close_connection(conn)

    init_db()

    return app