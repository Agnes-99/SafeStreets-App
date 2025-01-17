from flask import Blueprint, request, redirect, url_for,render_template, flash,session, current_app,jsonify, send_file
from .db import create_connection, insert_user, close_connection,insert_report,generate_report_id, get_posts_and_comments, update_likes, insert_post,insert_comment, delete_comment_db, delete_post_db, get_crime_stats_db, plot_png_db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
import random
import string
import datetime
import sqlite3
import base64
import re
import pandas as pd
import io
import matplotlib
import matplotlib.pyplot as plt
auth = Blueprint("auth",__name__)


#Landing of the app
@auth.route("/")
def login():
    return render_template("Login.html")

#Login Page
@auth.route ("/login", methods=["POST"])
def login_post():
    username =request.form["username"]
    password = request.form["password"]

    conn = create_connection(current_app.config["DATABASE"])
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE username=? ",(username,))
    user = cur.fetchone()
    close_connection(conn)

    if user and check_password_hash(user[6], password):
        session["username"] = username
        return redirect(url_for("auth.home")) 
    else:
        flash("Invalid username or password. Please try again.","danger")
        return redirect(url_for("auth.login"))


    
#Registration page
@auth.route("/register", methods=["GET","POST"])
def register():
   if request.method =="POST":

        #Get data from form
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        username = request.form["username"]
        cellnumber = request.form["cellnumber"]
        email = request.form["email"]
        password = request.form["password"]

       
        #Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        #Insert date into the databse
        conn = create_connection(current_app.config["DATABASE"])
        insert_user(conn,firstname,surname,username, cellnumber,email,hashed_password)
        close_connection(conn)

        flash ("Registration successful! Please log in with your username and password.","success")
        return redirect(url_for("auth.login"))
   
   return render_template("Registration.html")

#Home page
@auth.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("Home.html")

@auth.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out","info")
    return redirect(url_for("auth.login"))

#About Page
@auth.route("/about")
def about():
    return render_template("About.html")

#Confirmation Page
@auth.route("/confirmation")
def confirmation():
    return render_template("Confirmation.html")
   

#Emergency Page
@auth.route("/emergency")
def emergency():
    return render_template("Emergency.html")

#Report Page
@auth.route("/report")
def report():
    return render_template("Report.html")

#Reports-Pop-Up
@auth.route("/popup")
def popup():
    return render_template("Reports-pop-up.html")

#Final
@auth.route("/final")
def final():
    report_id=request.args.get("report_id")
    return render_template("Final.html", report_id=report_id)

#feedback
@auth.route("/feedback")
def feedback():
    return render_template("Feedback.html")

#Userfeed------------------------------------------------------------------
@auth.route("/userfeed")
def userfeed():

    if "username" not in session:
        flash("You need to log in first", "danger") 
        return redirect(url_for("auth.login"))

    username = session["username"]
    conn = create_connection(current_app.config["DATABASE"])
    
    posts, comments = get_posts_and_comments(conn)
    return render_template("userfeed.html", posts = posts, comments = comments, username=username)

@auth.route("/submit_post", methods=["POST"])
def submit_post():
    if "username" not in session:
        flash("You need to log in first", "danger") 
        return redirect(url_for("auth.login"))
    username = session["username"]
    conn = create_connection(current_app.config["DATABASE"])
    post_text = request.form["post_text"]
    post_id = insert_post(conn, username, post_text)
    return redirect("/userfeed")

@auth.route("/submit_comment", methods=["POST"])
def submit_comment():
    if "username" not in session:
        flash("You need to log in first", "danger") 
        return redirect(url_for("auth.login"))

    post_id = request.form["post_id"]
    username = session["username"]
    comment_text = request.form["comment_text"]
    conn = create_connection(current_app.config["DATABASE"])
    insert_comment(conn,post_id, username, comment_text)
    return redirect("/userfeed")

@auth.route('/like_post/<int:post_id>', methods=["POST"])
def like_post(post_id):
    if "username" not in session:
        flash("You need to log in first", "danger") 
        return redirect(url_for("auth.login"))

    username = session["username"]
    conn= create_connection(current_app.config["DATABASE"])
    update_likes(conn, post_id)
    return redirect("/userfeed")

@auth.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "username" not in session:
        flash("You need to log in first", "danger") 
        return redirect(url_for("auth.login"))
    
    conn = create_connection(current_app.config["DATABASE"])
    delete_post_db(conn, post_id)
    return redirect("/userfeed")

@auth.route('/delete_comment/<int:comment_id>', methods =["POST"])
def delete_comment(comment_id):
    if "username" not in session:
        flash("You need to log in first", "danger") 
        return redirect(url_for("auth.login"))
    conn = create_connection(current_app.config["DATABASE"])
    delete_comment_db(conn, comment_id)
    return redirect("/userfeed")
    
#------------------------------------------------------------------------------------------------
def save_files(files, folder):
    file_paths = []
    for file in files:
        if files and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(folder,filename)
            file.save(file_path)
            file_paths.append(filename)
    return file_paths


#REPORT PAGE--------------------------------------------------------------------------------------
#file uploads
def allowed_file(filename):
    allowed_extensions = {'png','jpg','jpeg','gif','mp4','avi','mov','ogg','wav','mp3'}
    return "." in filename and filename.rsplit(".",1)[1].lower() in allowed_extensions

def save_files(files, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

        file_paths =[]
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(folder, filename)
                file.save(file_path)
                file_paths.append(file_path)
        return file_paths
    
@auth.route("/upload", methods=["POST"])
def upload_files():
    if 'images[]' not in request.files and 'videos[]' not in request.files :
        flash("No file part")
        return redirect(request.url)

    images = request.files.getlist('images[]')
    videos = request.files.getlist('videos[]')

    images_folder =save_files(images, os.path.join(current_app.config["UPLOAD_FOLDER"], "images"))
    videos_folder =save_files(videos, os.path.join(current_app.config["UPLOAD_FOLDER"], "videos"))
            
    flash("Files uploaded successfully!")
    return redirect(url_for('auth.report'))



#Submit report
@auth.route("/submit_report", methods=["POST"])
def submit_report():

    data = request.get_json()
    print("Recieved data:", data)

    username = session.get("username")
    print("Username:", username)

    if not username:
        return jsonify({"success": False, "message":"User not logged in"}), 403


    conn = create_connection(current_app.config["DATABASE"])
    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM Users WHERE username =?", (username,))
        user =cur.fetchone()

        if not user:
                return jsonify ({"success": False, "message":"User not found"}), 404

        user_id =user[0]
        print("User ID:", user_id)

        crime_type = data.get("crime_type")
        timing = data.get("crime_date")
        crime_status = "PENDING"
        description =data.get("description")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        images= data.get("images",[])
        videos = data.get("videos",[])

        image_paths = ",".join(images) if images else ""
        videos_paths = ",".join(videos) if videos else ""
        
        report_id = generate_report_id()
        report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_report(conn,report_id, user_id, crime_type,timing,description,image_paths,videos_paths,crime_status, latitude,longitude,report_date)
        return jsonify({"success": True , "report_id":report_id})

    except sqlite3.Error as e:
        print(f"Insert error: {e}")
        return jsonify({"success":False, "message":"Error occcured while inserting the report"}), 500
    finally:
        close_connection(conn)


@auth.route("/account")
def account():

    if "username" not in session:
        flash("You need to log in first")
        return redirect(url_for("auth.login"))

    username = session["username"]
    conn = conn = create_connection(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row

    #fetch information
    user_query = "SELECT * FROM Users WHERE username = ?"
    user = conn.execute(user_query,(username,)).fetchone()
   
    if not user:
        return "User not found", 404
    
    user_id =int(user['user_id'])

    #fetch report information
    report_query = "SELECT * FROM Reports WHERE user_id = ?"
    reports = conn.execute(report_query,(user_id,)).fetchall()
    conn.close()
    return render_template("Account.html", user = user, reports = reports)

@auth.route("/stats")
def getStats():

    username = session["username"]
    if "username" not in session:
        flash("You need to log in first")
        return redirect(url_for("auth.login"))
    conn = create_connection(current_app.config["DATABASE"])

    #fetch information
    rows = get_crime_stats_db(conn)
    df =  pd.DataFrame( rows, columns =["crime_category", "april2020_june2020", "april2021_june2021",
                                     "april2022_june2022", "april2023_june2023", "april2024_june2024",
                                     "count_diff", "percentage_change"])

    table_html =df.to_html(classes ="table table-striped", index = False)
    return render_template("table.html", table_html=table_html)

@auth.route("/plot.png")
def plot_png():
     
    username = session["username"]
    if "username" not in session:
        flash("You need to log in first")
        return redirect(url_for("auth.login"))
    
    conn = create_connection(current_app.config["DATABASE"])
    rows = plot_png_db(conn)

    df = pd.DataFrame(rows, columns=["crime_category", "april2020_june2020", "april2021_june2021",
                                     "april2022_june2022", "april2023_june2023", "april2024_june2024"])

    # Limit to the first 5 crime categories for less clutter
    df_subset = df.head(5)  
    plt.figure(figsize =(10, 6))
    for column in df_subset.columns[1:]:
        plt.plot(df_subset["crime_category"], df_subset[column], label=column)
    
    plt.title("Crime Statistics Over Time : Top 5")
    plt.xlabel("Crime Category")
    plt.ylabel("Incidents")
    plt.legend()
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format ="png")
    img.seek(0)
    return send_file(img, mimetype="image/png")

    