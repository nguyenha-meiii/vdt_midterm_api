import unittest
from unittest import mock
from bson import ObjectId
from run import app, students_collection

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_list_students(self):
        with mock.patch('run.students_collection.find') as mock_find:
            mock_find.return_value = [
                {
                    '_id': ObjectId(),
                    'fullName': 'John Doe',
                    'doB': '1990',
                    'gender': 'Male',
                    'school': 'ABC School',
                    'major': 'Computer Science'
                },
                {
                    '_id': ObjectId(),
                    'fullName': 'Jane Smith',
                    'doB': '1995',
                    'gender': 'Female',
                    'school': 'XYZ School',
                    'major': 'Data Science'
                }
            ]

            response = self.app.get('/api/students')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 2)
            self.assertEqual(response.json[0]['fullName'], 'John Doe')
            self.assertEqual(response.json[1]['major'], 'Data Science')

    def test_create_student(self):
        with mock.patch('run.students_collection.insert_one') as mock_insert_one:
            mock_insert_one.return_value = mock.Mock(inserted_id=ObjectId())

            data = {
                "no": 22,
                "fullName": "Nguyen Van CDE",
                "doB": "2001",
                "gender": "Nam",
                "school": "NEUST"
            }

            response = self.app.post('/api/students', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Student created successfully')

    def test_get_student_by_id_found(self):
        student_id = str(ObjectId())
        with mock.patch('run.students_collection.find_one') as mock_find_one:
            mock_find_one.return_value = {
                '_id': ObjectId(student_id),
                'fullName': 'Nguyen Van CDE',
                'doB': '2001',
                'gender': 'Nam',
                'school': 'NEUST',
                'major': 'Computer Science'
            }

            response = self.app.get(f'/api/students/{student_id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['fullName'], 'Nguyen Van CDE')

    def test_get_student_by_id_not_found(self):
        with mock.patch('run.students_collection.find_one') as mock_find_one:
            mock_find_one.return_value = None
            student_id = str(ObjectId())

            response = self.app.get(f'/api/students/{student_id}')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['message'], 'Student not found')

    def test_update_student(self):
        student_id = str(ObjectId())
        with mock.patch('run.students_collection.update_one') as mock_update_one:
            mock_update_one.return_value = mock.Mock(modified_count=1)
            data = {
                "no": 55,
                "fullName": "Nguyen Van CDF",
                "doB": "2001",
                "gender": "gioi tinh thu 3",
                "school": "NEUST"
            }

            response = self.app.put(f'/api/students/{student_id}', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Student updated successfully')

    def test_delete_student(self):
        student_id = str(ObjectId())
        with mock.patch('run.students_collection.delete_one') as mock_delete_one:
            mock_delete_one.return_value = mock.Mock(deleted_count=1)

            response = self.app.delete(f'/api/students/{student_id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Student deleted successfully')

if __name__ == '__main__':
    unittest.main()
