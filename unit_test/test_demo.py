import unittest
from unittest.mock import patch, Mock

from run import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('run.students_collection.find')
    def test_list_students(self, mock_find):
        mock_find.return_value = [
            {
                '_id': '1',
                'Name': 'John Doe',
                'YearOfBirth': 1990,
                'Sex': 'Male',
                'School': 'ABC School',
                'Major': 'Computer Science'
            },
            {
                '_id': '2',
                'Name': 'Jane Smith',
                'YearOfBirth': 1995,
                'Sex': 'Female',
                'School': 'XYZ School',
                'Major': 'Data Science'
            }
        ]

        response = self.app.get('/api/students')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['Name'], 'John Doe')
        self.assertEqual(response.json[1]['Major'], 'Data Science')

    @patch('run.students_collection.insert_one')
    def test_create_student(self, mock_insert_one):
        mock_insert_one.return_value = Mock(inserted_id='mock_id')

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

    @patch('run.students_collection.find_one')
    def test_get_student_by_id(self, mock_find_one):
        mock_find_one.return_value = {
            '_id': 'mock_id',
            'no': 22,
            'fullName': 'Nguyen Van CDE',
            'doB': '2001',
            'gender': 'Nam',
            'school': 'NEUST'
        }

        response = self.app.get('/api/students/mock_id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['_id'], 'mock_id')

    @patch('run.students_collection.update_one')
    def test_update_student(self, mock_update_one):
        mock_update_one.return_value = Mock()

        updated_data = {
            "no": 55,
            "fullName": "Nguyen Van CDF",
            "doB": "2001",
            "gender": "gioi tinh thu 3",
            "school": "NEUST"
        }
        response = self.app.put('/api/students/mock_id', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Student updated successfully')

    @patch('run.students_collection.delete_one')
    def test_delete_student(self, mock_delete_one):
        mock_delete_one.return_value = Mock(deleted_count=1)

        response = self.app.delete('/api/students/mock_id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Student deleted successfully')


if __name__ == '__main__':
    unittest.main()
