import sqlite3
import string
import random
import os


# Function to get connection to the database
def create_connection(db_file):

    if not os.path.isfile(db_file):
        print(f"The database file path does not exist: {db_file}")

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database {db_file}")
    except (sqlite3.Error, OSError) as e:
        print(f"Error: {e}, could not connect to database")
    return conn

# Function to create tables
def create_tables(conn):
    if conn is None:
        print("Connection is not established")
        return

    try:
        cur = conn.cursor()

        # Create user table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                surname TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                cellnumber TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create report table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Reports(
                report_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                crime_type TEXT NOT NULL,
                timing TEXT NOT NULL,
                description TEXT,
                images BLOB,
                videos BLOB,
                crime_status TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES Users(user_id)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Posts(
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                post_text TEXT,
                likes INTEGER DEFAULT 0,
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(username) REFERENCES Users(username)  
             )
        ''')

        cur. execute('''
            CREATE TABLE IF NOT EXISTS Comments(
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                username TEXT,
                comment_text TEXT,
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(post_id) REFERENCES Posts(post_id),
                FOREIGN KEY(username) REFERENCES Posts(username)
                )
          ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Location(
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_lat REAL,
            location_lon REAL,
            address TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Category(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS ReportCategory(
            report_id TEXT,
            category_id INTEGER,
            PRIMARY KEY (report_id, category_id),
            FOREIGN KEY (report_id) REFERENCES Reports(report_id),
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        )
        ''')

        conn.commit()
        print("Tables created successfully.")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

    finally:
        cur.close() if cur else None



# Function to insert a user
def insert_user(conn, firstname, surname, username, cellnumber, email, hashed_password):
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Users (firstname, surname, username, cellnumber, email, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (firstname, surname, username, cellnumber, email, hashed_password))
        
        conn.commit()
        print("User inserted successfully.")
       
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
    finally:
        cur.close() if cur else None

# Function to insert a report
def insert_report(conn, report_id, user_id, crime_type, timing, description, images, videos, crime_status, latitude, longitude, report_date):
    
    cur = None

    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Reports(report_id, user_id, crime_type, timing, description, images, videos, crime_status, latitude, longitude,report_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (report_id, user_id, crime_type, timing, description, images, videos, crime_status, latitude, longitude, report_date))
        
        conn.commit()
        print("Report inserted successfully")

    except sqlite3.Error as e:
        print(f"Error inserting report: {e}")
    finally:
        cur.close() if cur else None

#Function to insert posts
def insert_post(conn,username,post_text):
    cur = None
    post_id = None

    try: 
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Posts (username,post_text) VALUES (?,?)
            ''', (username, post_text))
        conn.commit()
        print("Post inserted successfully")
        post_id = cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting post: {e}")
    finally:
        cur.close() if cur else None
    return post_id

#Function to insert Comments
def insert_comment(conn, post_id, username ,comment_text):
    cur = None

    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Comments (post_id, username, comment_text) VALUES (?,?,?)
            ''',(post_id,username,comment_text))
        conn.commit()
        print("Comment inserted successfully")
    except sqlite3.Error as e:
        print(f"Error inserting comment: {e}")
    finally:
        cur.close() if cur else None

#Function to update likes
def update_likes(conn, post_id):
    cur = None

    try: 
        cur = conn.cursor()
        cur.execute('''
            UPDATE Posts SET likes = likes + 1 WHERE post_id = ?
            ''',(post_id,))
        conn.commit()
        print("Likes updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating likes: {e}")
    finally:
        cur.close() if cur else None


#Function to retrieve posts and comments
def get_posts_and_comments(conn):

    cur = None
    posts = []
    comments = []

    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM Posts ORDER BY post_id DESC
            ''')
        posts = cur.fetchall()
        cur.execute('''
            SELECT * FROM Comments
            ''')
        comments = cur.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching Posts and comments: {e}")
    finally:
        cur.close() if cur else None
    return posts, comments

#function to delete post
def delete_post_db(conn, post_id):

    cur = None
    
    try:
        cur=conn.cursor()
        cur.execute('''
            DELETE FROM Posts WHERE post_id=?
        ''',(post_id,))
        conn.commit()
        print("Post deleted successfully")
    except sqlite3.Error as e:
        print(f"Error deleting post: {e}")
    finally:
        cur.close() if cur else None

#function to delete comment
def delete_comment_db(conn, comment_id):
    cur = None
    try:
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM Comments WHERE comment_id =?
        ''', (comment_id,))
        conn.commit()
        print("Comment deleted successfully")
    except sqlite3.Error as e:
        print(f"Error deleting comment: {e}")
    finally:
        cur.close() if cur else None

# Close the database connection
def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed")

# Generate report ID
def generate_report_id(length=6):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))
