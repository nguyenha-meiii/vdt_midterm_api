from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import json
import os


MONGO_URI = os.getenv('DATABASE_PORT', 'mongodb+srv://root:hello123@vdt.2w2zlck.mongodb.net/?retryWrites=true&w=majority&appName=vdt')
JWT_SECRET = os.getenv('JWT_SECRET', 'VDT2024')


app = Flask(__name__)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})


logging.basicConfig(level=logging.INFO)


def rate_limit_exceeded(e):
    return jsonify({"error": "Too many requests"}), 409


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute"],
    storage_uri="memory://"
)


app.config['RATELIMIT_HEADERS_ENABLED'] = True
app.register_error_handler(429, rate_limit_exceeded)


limiter.init_app(app)


def get_db():
    client = MongoClient(MONGO_URI)
    db = client["test"]
    return db


# Routes
@app.route('/')
@limiter.limit("10 per minute")
def ping_server():
    db = get_db()
    trainees_collection = db.trainees
    trainees = list(trainees_collection.find({}, {'_id': 1, 'name': 1, 'email': 1, 'gender': 1, 'school': 1}))
    for trainee in trainees:
        trainee['_id'] = str(trainee['_id'])
    logging.info("Hello123")
    logging.info(trainees_collection)
    return "Welcome to trainees list."


@app.route('/api/trainees', methods=['GET'])
@limiter.limit("10 per minute")
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
@limiter.limit("10 per minute")
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
@limiter.limit("10 per minute")
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
@limiter.limit("10 per minute")
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
@limiter.limit("10 per minute")
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

