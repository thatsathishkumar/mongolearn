from flask import *
from pymongo import *
from bson.objectid import *

client = MongoClient("localhost", 27017)
client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000")
db = client.datambox
people = db.people


app = Flask(__name__)
app.secret_key = "hello"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        
        username = request.form["username"]
        age = request.form["age"]
        
    
        data_json = {
            "name" : username,
            "age" : age
        }
    
        print("\n", data_json, "\n")
    
        people.insert_one(data_json)
    
        return redirect(url_for("success"))
    
    return render_template("login.html")

@app.route("/datam", methods = ["POST", "GET"])
def datam():
    # people.findAndModify(
    #     {
    #         query: { _id: name },
    #         update: { $inc: { seq: 1 } },
    #         new: true
    #     }
    # );
    for person in people.find():
        print("\n", person, "\n")
    return render_template("datam.html", people = people.find())


@app.post("/<id>/delete")
def delete(id):
    people.delete_one({"_id" : ObjectId(id)})
    return redirect(url_for("datam" , i = 1))


@app.route("/success", methods = ["POST", "GET"])
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug = True)