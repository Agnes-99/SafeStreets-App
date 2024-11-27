from flask import Flask
import os
from .routes import auth 
from dashboard import create_dashboard

def create_app ():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config["DATABASE"] = "safestreets.db"
    app.config["UPLOAD_FOLDER"] ="../static/uploads"
    app.config["ALLOWED_EXTENSIONS"] = {'png','jpg','jpeg','gif','mp4','avi','mov','ogg','wav','mp3'}
    app.secret_key ="Apples&Bananas"

    app.register_blueprint(auth)
    create_dashboard(app)# intergrates Dash with Flask

    #initialize database 
    from app.db import create_connection, create_tables, close_connection

    def init_db():
        conn = create_connection(app.config["DATABASE"])
        if conn:
            create_tables(conn)
            close_connection(conn)

    init_db()

    return app