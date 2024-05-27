import unittest
import json
import requests

URL_TEST = "http://localhost:5001/api/students"

# class TestAPI(unittest.TestCase):
#     def setUp(self):
#         # Create a sample student for testing purposes
#         data = {
#             "no": 22,
#             "fullName": "Nguyen Van CDE",
#             "doB": "2001",
#             "gender": "Nam",
#             "school": "NEUST"
#         }
#         res = requests.post(URL_TEST, json=data)
#         if res.status_code != 200:
#             print(f"Error creating student: {res.text}")

#         self.assertEqual((res.json())['message'], 'Student created successfully')
#         self._id = (res.json())['id']

#     def tearDown(self):
#         # Delete the sample student created in setUp
#         res = requests.delete(f"{URL_TEST}/{self._id}").json()
#         self.assertEqual(res['message'], 'Student deleted successfully')

#     def test_get_students(self):
#         # GET /api/students
#         res = requests.get(URL_TEST)
#         self.assertEqual(res.status_code, 200)
#         self.assertGreater(len(res.json()), 0)

#     def test_create_student(self):
#         data = {
#             "no": 44,
#             "fullName": "Nguyen Van A",
#             "doB": "2000",
#             "gender": "Nam",
#             "school": "HUST"
#         }
#         res = requests.post(URL_TEST, json=data)
#         self.assertEqual(res.status_code, 200)
#         self.created_id = res.json()['id']
#         self.assertEqual(res.json()['message'], 'Student created successfully')

#     def test_get_student_by_id(self):
#         res = requests.get(f"{URL_TEST}/{self._id}")
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['_id'], self._id)
#         self.assertGreater(len(res.json()), 0)

#     def test_update_student(self):
#         updated_data = {
#             "no": 55,
#             "fullName": "Nguyen Van CDF",
#             "doB": "2001",
#             "gender": "gioi tinh thu 3",
#             "school": "NEUST"
#         }
#         res = requests.put(f"{URL_TEST}/{self._id}", json=updated_data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.json()['message'], 'Student updated successfully')

#     def test_delete_student(self):
#         # Ensure we create a student to delete
#         data = {
#             "no": 44,
#             "fullName": "Nguyen Van A",
#             "doB": "2000",
#             "gender": "Nam",
#             "school": "HUST"
#         }
#         res = requests.post(URL_TEST, json=data)
#         self.assertEqual(res.status_code, 200)
#         created_id = res.json()['id']
#         self.assertEqual(res.json()['message'], 'Student created successfully')

#         # Delete the newly created student
#         response = requests.delete(f'{URL_TEST}/{created_id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['message'], 'Student deleted successfully')

#         # Check if the student is really deleted
#         response = requests.get(f'{URL_TEST}/{created_id}')
#         self.assertEqual(response.status_code, 404)

# if __name__ == "__main__":
#     test_order = ["setUp", "test_get_students", "test_create_student", "test_get_student_by_id", "test_update_student", "test_delete_student", "tearDown"] 
#     test_loader = unittest.TestLoader()
#     test_loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
#     unittest.main(testLoader=test_loader)

class TestAPI(unittest.TestCase):
    def setUp(self):
        data = {
            "no": 22,
            "fullName": "Nguyen Van CDE",
            "doB": "2001",
            "gender": "Nam",
            "school": "NEUST"
        }
        res = requests.post(URL_TEST, json=data)
        if res.status_code != 200:
            print(f"Error creating student: {res.text}")
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        self.assertEqual(res_json['message'], 'Student created successfully')
        self._id = res_json['id']

    def tearDown(self):
        res = requests.delete(f"{URL_TEST}/{self._id}")
        if res.status_code != 200:
            print(f"Error deleting student: {res.text}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['message'], 'Student deleted successfully')

    def test_get_students(self):
        res = requests.get(URL_TEST)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()), 0)

    def test_create_student(self):
        data = {
            "no": 44,
            "fullName": "Nguyen Van A",
            "doB": "2000",
            "gender": "Nam",
            "school": "HUST"
        }
        res = requests.post(URL_TEST, json=data)
        self.assertEqual(res.status_code, 200)
        self.created_id = res.json()['id']
        self.assertEqual(res.json()['message'], 'Student created successfully')

    def test_get_student_by_id(self):
        res = requests.get(f"{URL_TEST}/{self._id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['_id'], self._id)
        self.assertGreater(len(res.json()), 0)

    def test_update_student(self):
        updated_data = {
            "no": 55,
            "fullName": "Nguyen Van CDF",
            "doB": "2001",
            "gender": "gioi tinh thu 3",
            "school": "NEUST"
        }
        res = requests.put(f"{URL_TEST}/{self._id}", json=updated_data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['message'], 'Student updated successfully')

    def test_delete_student(self):
        data = {
            "no": 44,
            "fullName": "Nguyen Van A",
            "doB": "2000",
            "gender": "Nam",
            "school": "HUST"
        }
        res = requests.post(URL_TEST, json=data)
        self.assertEqual(res.status_code, 200)
        created_id = res.json()['id']
        self.assertEqual(res.json()['message'], 'Student created successfully')

        response = requests.delete(f'{URL_TEST}/{created_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Student deleted successfully')

        response = requests.get(f'{URL_TEST}/{created_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    test_order = ["setUp", "test_get_students", "test_create_student", "test_get_student_by_id", "test_update_student", "test_delete_student", "tearDown"] 
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=test_loader)