import io
import unittest
from flask import json
from app import create_app
from extensions import db
from config import TestConfig

class TestFlaskApi(unittest.TestCase):

    def create_app(self):
        """Create an instance of the app with the testing configuration."""
        app = create_app(TestConfig)
        return app

    def setUp(self):
        """Set up the application context and test client before each test."""
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Tear down the database and application context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        """Test user registration functionality."""
        response = self.client.post('/api/register/', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.json['message'])

    def test_duplicate_user(self):
        """Test registration of duplicate usernames."""
        self.test_register_user()  # Register a user first
        response = self.client.post('/api/register/', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already taken', response.json['message'])

    def test_create_project(self):
        """Test project creation functionality."""
        self.test_register_user()  # Ensure a user is registered
        response = self.client.post('/api/create_project/', json={
            'username': 'testuser',
            'project_type': 'Image Classification',
            'name': 'Test Project'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Project created successfully', response.json['message'])

    def test_upload_image(self):
        """Test image upload functionality."""
        self.test_create_project()  # Ensure a project is available
        response = self.client.post('/api/upload_image/1/', data={
            'file': (io.BytesIO(b"test image data"), 'test.jpg')
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Image uploaded successfully', response.json['message'])

    def test_analyze_project(self):
        project_id = self.test_create_project()
        self.test_upload_image()
        response = self.client.get(f'/api/analyze_project/{project_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_feature_size', response.json)

    def test_configure_training(self):
        project_id = self.test_create_project()
        response = self.client.post(f'/api/configure_training/{project_id}/', json={
            'learning_rate': 0.01,
            'epochs': 10,
            'batch_size': 32
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Training configuration updated successfully', response.json['message'])

    def test_enqueue_training(self):
        project_id = self.test_create_project()
        self.test_configure_training()
        response = self.client.post(f'/api/enqueue_training/{project_id}/')
        self.assertEqual(response.status_code, 202)
        self.assertIn('Training task enqueued', response.json['message'])

    def test_get_training_results(self):
        project_id = self.test_create_project()
        self.test_enqueue_training()
        response = self.client.get(f'/api/training_results/{project_id}/')
        self.assertEqual(response.status_code, 200)
        # Check if results are returned or not found message
        assert 'accuracy' in response.json[0] or 'No training results found' in response.json['error']

    def test_delete_image(self):
        """Test image deletion functionality."""
        self.test_upload_image()  # Ensure an image is uploaded
        response = self.client.delete('/api/delete_image/testuser/1/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Image deleted successfully', response.json['message'])

    def test_delete_project(self):
        """Test project deletion functionality."""
        self.test_create_project()  # Ensure a project is created
        project_id = 1  # Assuming first project has ID 1
        response = self.client.delete(f'/api/delete_project/{project_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Project deleted successfully', response.json['message'])
    
if __name__ == '__main__':
    unittest.main()
