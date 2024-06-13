from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import json
import os

# Load environment variables
MONGO_URI = os.getenv('DATABASE_PORT', 'mongodb+srv://root:hello123@vdt.2w2zlck.mongodb.net/?retryWrites=true&w=majority&appName=vdt')
JWT_SECRET = os.getenv('JWT_SECRET', 'VDT2024')

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# Set up logging
logging.basicConfig(level=logging.INFO)

# MongoDB configuration function
def get_db():
    client = MongoClient(MONGO_URI)
    db = client["test"]
    return db

# Routes 

@app.route('/')
def ping_server():
    db = get_db()
    trainees_collection = db.trainees
    # lỗi không connect được vs database
    trainees = list(trainees_collection.find({}, {'_id': 1, 'name': 1, 'email': 1, 'gender': 1, 'school': 1}))
    for trainee in trainees:
        trainee['_id'] = str(trainee['_id'])
    logging.info("Hello123")  # sử dụng logging thay vì print
    logging.info(trainees_collection)  # sử dụng logging thay vì print
    return "Welcome to trainees list."

@app.route('/api/trainees', methods=['GET'])
def get_trainees():
    try:
        db = get_db()
        trainees_collection = db.trainees
        trainees = list(trainees_collection.find({}, {'_id': 1, 'name': 1, 'email': 1, 'gender': 1, 'school': 1}))
        for trainee in trainees:
            trainee['_id'] = str(trainee['_id'])  # Convert ObjectId to string

        formatted_response = '[' + ',\n'.join(json.dumps(trainee, ensure_ascii=False) for trainee in trainees) + ']'
        response = Response(formatted_response, content_type='application/json; charset=utf-8')
        return response
    except Exception as e:
        logging.error(f"Error fetching trainees: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/trainees', methods=['POST'])
def create_trainee():
    try:
        db = get_db()
        trainees_collection = db.trainees
        data = request.json
        result = trainees_collection.insert_one(data)
        return jsonify({'message': 'Trainee created successfully', 'id': str(result.inserted_id)}), 200
    except Exception as e:
        logging.error(f"Error creating trainee: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/trainees/<string:id>', methods=['GET'])
def get_trainee(id):
    try:
        db = get_db()
        trainees_collection = db.trainees
        trainee = trainees_collection.find_one({'_id': ObjectId(id)}, {'_id': 1, 'name': 1, 'email': 1, 'gender': 1, 'school': 1})
        if trainee:
            trainee['_id'] = str(trainee['_id'])  # Convert ObjectId to string
            return jsonify(trainee), 200
        else:
            return jsonify({'message': 'Trainee not found'}), 404
    except Exception as e:
        logging.error(f"Error fetching trainee with ID {id}: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/trainees/<string:id>', methods=['PUT'])
def update_trainee(id):
    try:
        db = get_db()
        trainees_collection = db.trainees
        data = request.json
        data.pop('_id', None)
        result = trainees_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count == 1:
            return jsonify({'message': 'Trainee updated successfully'}), 200
        else:
            return jsonify({'message': 'Trainee not found'}), 404
    except Exception as e:
        logging.error(f"Error updating trainee with ID {id}: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/trainees/<string:id>', methods=['DELETE'])
def delete_trainee(id):
    try:
        db = get_db()
        trainees_collection = db.trainees
        result = trainees_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Trainee deleted successfully'}), 200
        else:
            return jsonify({'message': 'Trainee not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting trainee with ID {id}: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
