from pymongo.mongo_client import MongoClient
from flask import Flask , jsonify , request
from flask_basicauth import BasicAuth
from flask_cors import CORS

uri = "mongodb+srv://phuriphat:P_Phu20112546@product-detail.vyje4og.mongodb.net/?retryWrites=true&w=majority&appName=product-detail"

try:
    client = MongoClient(uri)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products",methods=["GET"])
def get_all_products():
    try:
        db = client["product-detail"]
        collection = db["product_info"]
        all_product = list(collection.find())
        return jsonify(all_product),200
    except Exception as e:
        print(e)

@app.route("/product",methods=["POST"])
def add_product():
    try:
        db = client["product-detail"]
        collection = db["product_info"]
        data = request.get_json()
        if(collection.find_one({"_id" : data.get("_id")})):
            return jsonify({"error":"Cannot create new product"}),404
        collection.insert_one(data)
        return jsonify(data),200
    except Exception as e:
            print(e)

@app.route("/product/<string:pro_id>", methods=["PUT"])
def update_product(pro_id):
    try:
        db = client["product-detail"]
        collection = db["product_info"]
        data = request.get_json()
        if(collection.find_one({"_id" : pro_id})):
            print("Found")
            collection.update_one({"_id":pro_id}, {"$set": data})
            return jsonify(data),200
        else:
            return jsonify({"error":"Product not found"}),404
        
    except Exception as e:
        print(e)


@app.route("/product/<string:pro_id>", methods=["DELETE"])
def delete_product(pro_id):
    try:
        db = client["product-detail"]
        collection = db["product_info"]
        if(collection.find_one({"_id" : pro_id})):
            collection.delete_one({"_id" : pro_id})
            return jsonify({"message":"Product deleted successfully"}),200
        else:
            return jsonify({"error":"Product not found"}),404
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3000,debug=True)