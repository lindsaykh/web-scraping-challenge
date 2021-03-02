# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)


# Use PyMongo to establish Mongo connection to database called mars_db
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    # Return template by looking for files in templates folder and refer to mars dict as mars for simplicity
    return render_template("index.html", mars=mars_dict)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
  
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_data, upsert=True)

    print("Data Uploaded!")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)