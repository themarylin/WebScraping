from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

@app.route("/")
def index():
    mars = client.mars_db
    collection = mars.table
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = client.mars_db 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)