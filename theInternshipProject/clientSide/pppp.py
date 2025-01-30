from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://tljne:4BMNBXEZS7gqrnqM@tljne.gw0jc.mongodb.net/tljne"
db = PyMongo(app).db

app.config['db'] = db
app.config['SECRET_KEY'] = 'dc8ce0faf1677dfe9e71c52d5037428d'



@app.route("/")  # Added a route for the homepage
def index():
    #  Get the data from the 'poem' collection.  Important: check if it exists!
    poem_collection = db.interviews  # Access the 'poem' collection directly.

    try:
        poems = list(poem_collection.find())  # Fetch all poems as a list of dictionaries.  Error-handling!

    except Exception as e:
        # Log the error, then render a friendly message for the user.
        import logging
        logging.exception(f"Error fetching data: {e}")
        return render_template("error.html", error_message=f"An error occurred: {e}"), 500


    return render_template("index.html", poems=poems)  # Pass the list to the template


if __name__ == "__main__":
    app.run(debug=True)