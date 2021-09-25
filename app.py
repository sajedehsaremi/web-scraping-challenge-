from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd
import time

# create an instance of Flask
app = Flask(__name__)

# use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/MissionToMars_DB")

import pymongo
 

 


# Rout to render index.html template using data from Mongo
@app.route("/")
def home():
    print("-----------------------------Home")
    mars_information = mongo.db.marsdata.find_one()
    return render_template("index.html", mars_information=mars_information)

# Rout that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # run the scrape function
    mars_database = mongo.db.marsdata
    mars_information = scrape_mars.scrape()
    # update the Mongo database using update and upsert=true
    mars_database.update({}, mars_information, upsert=True)
    return redirect('/')

# Redirect back to home page
    # return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)