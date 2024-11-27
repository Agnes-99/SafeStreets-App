import os
from app import create_app
from flask_cors import CORS


# Initialize the Flask app
app = create_app()
CORS(app, origins=["https://agnes123.pythonanywhere.com"])

if __name__ == "__main__":

    app.run(debug=True) 
   
    if not os.path.isfile(db_file):
        print(f"The database file path does not exist: {db_file}")
