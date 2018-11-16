from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/render_from_mongo_db"
mongo = PyMongo(app)


@app.route("/")
def index():

    output = mongo.db.mars_db.find_one()

    return render_template("index.html", output=output)


@app.route("/scrape")
def scraper():

    output = scrape()
    mars_db = mongo.db.mars_db
    mars_db.update({},output,upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
