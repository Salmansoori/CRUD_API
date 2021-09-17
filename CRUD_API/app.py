from flask import Flask, json
from flask_pymongo import PyMongo
from flask import jsonify, request
import urllib 
from bson.json_util import dumps
from bson.objectid import ObjectId

app= Flask(__name__)


## mongodb connection with flask

app.config['MONGO_URI']="Your database mongo uri"

mongo = PyMongo(app)
db=mongo.db
        

@app.route("/")
def home():
    return "hello world"

# Create record    

@app.route("/create",methods=["POST"])
def create():
    _json = request.json
    name = _json['name']
    image = _json['image']
    summary = _json['summary'] 
    if request.method=="POST":
        #cluster0 is the name of my database
        db.cluster0.insert_one({ "name":name, "image":image, "summary":summary })
        return "success"
    return "error msg"    


#read record

@app.route('/read')
def show():
	users = db.cluster0.find()
	resp = dumps(users)
	return resp


#update record

@app.route("/update/<id>",methods=["PUT"])    
def update(id):
    id = id
    _json = request.json
    name= _json['name']
    image = _json['image']
    summary =_json['summary']
    if request.method=="PUT":
        db.cluster0.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {'name': name, 'image': image, 'summary': summary}})
        resp=jsonify("record updated successfully")
        return resp
    return "error"    


#delete record

@app.route("/delete/<id>",methods=["DELETE"])    
def delete(id):
    db.cluster0.delete_one({'_id': ObjectId(id)})
    resp = jsonify('record deleted successfully')
    return resp

    

if __name__ == "__main__":
    app.run(debug=True)

