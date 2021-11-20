from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)

# database connection
app.config['MONGO_URI']='mongodb://localhost/agency'
mongo = PyMongo(app)

CORS(app)

# create collection
db = mongo.db.advertisementrecords

# add records
@app.route('/add', methods=['POST'])
def createadvertisement():
    id = db.insert({
        'client': request.json['client'],
        'description': request.json['description'],
        'businesstype': request.json['businesstype'],
        'date': request.json['date'],
        'deliverydate': request.json['deliverydate'],
        'cost': request.json['cost'],
        'status': request.json['status']
    })
    return jsonify({'id': str(ObjectId(id)), 'msg': "Ads Added Successfully"})

# get records
@app.route('/', methods=['GET'])
def getadvertisement():
    ads = []
    for doc in db.find():
        ads.append({
            '_id': str(ObjectId(doc['_id'])),
            'client': doc['client'],
            'description': doc['description'],
            'businesstype': doc['businesstype'],
            'date': doc['date'],
            'deliverydate': doc['deliverydate'],
            'cost': doc['cost'],
            'status': doc['status'],
        })
        return jsonify(ads)

# update records
@app.route('/update/<id>', methods=['PUT'])
def updateadvertisement(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
            'client': request.json['client'],
            'description': request.json['description'],
            'businesstype': request.json['businesstype'],
            'date': request.json['date'],
            'deliverydate': request.json['deliverydate'],
            'cost': request.json['cost'],
            'status': request.json['status']
    }})
    return jsonify({'msg': "ads update successfully"})

# delete records
@app.route('/delete/<id>', methods=['DELETE'])
def deleteadvertisement(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "ad delete successfully"})

if __name__ == '__main__':
    app.run(debug=True)