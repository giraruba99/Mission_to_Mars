# lets first import our dependancies

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
#from app import app

# next, we are setting our flask

app = Flask(__name__)

# use flask_pymongo to set up mongo connections

#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# First, let's define the route for the HTML page. In our script, type the following:

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Let's now create our scraping rout, and it will be tied to a button that will run the code when clicked

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    #return "Successful"
    return render_template("scrape.html", mars=mars_data)
    
# let's now write a code that tells flask to run

if __name__ == "__main__":
    app.run(debug=True)