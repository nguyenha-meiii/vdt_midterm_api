
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
# Set up logging
logging.basicConfig(level=logging.INFO)

# MongoDB configuration
client = MongoClient("mongodb://mongo_db:27017/")
db = client["student_db"]
students_collection = db["students"]

# Routes

# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        students = list(students_collection.find({}, {'_id': 1,'no': 1, 'fullName': 1, 'doB': 1, 'gender': 1, 'school': 1, 'major': 1}))
        for student in students:
            student['_id'] = str(student['_id'])  # Convert ObjectId to string
        return jsonify(students), 200
    except Exception as e:
        logging.error(f"Error fetching students: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Create a new student
@app.route('/api/students', methods=['POST'])
def create_student():
    try:
        data = request.json
        print(data)
        result = students_collection.insert_one(data)
        return jsonify({'message': 'Student created successfully', 'id': str(result.inserted_id)}), 200
    except Exception as e:
        logging.error(f"Error creating student: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Get a student by ID
@app.route('/api/students/<string:id>', methods=['GET'])
def get_student(id):
    try:
        student = students_collection.find_one({'_id': ObjectId(id)}, {'_id': 1, 'fullName': 1, 'doB': 1, 'gender': 1, 'school': 1, 'major': 1})
        if student:
            student['_id'] = str(student['_id'])  # Convert ObjectId to string
            return jsonify(student), 200
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        logging.error(f"Error fetching student with ID {id}: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Update a student by ID
@app.route('/api/students/<string:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.json
        # Remove the _id field from the update data to prevent modifying the immutable _id field
        data.pop('_id', None)
        result = students_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count == 1:
            return jsonify({'message': 'Student updated successfully'}), 200
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        logging.error(f"Error updating student with ID {id}: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Delete a student by ID
@app.route('/api/students/<string:id>', methods=['DELETE'])
def delete_student(id):
    try:
        result = students_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Student deleted successfully'}), 200
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting student with ID {id}: {e}")
        return jsonify({'message': 'Internal server error'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
