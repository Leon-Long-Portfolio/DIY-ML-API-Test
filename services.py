from flask import jsonify, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
import queue
from models import User, Project, Image, TrainingConfig, TrainingResult, InferenceResult, db
from datetime import datetime

# Initialize queues for managing asynchronous tasks
training_queue = queue.Queue()
inference_queue = queue.Queue()

# Helper function to check allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Register a new user
def register_user(request):
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Retrieve user by username
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_info = {
        'username': user.username,
        'user_id': user.id,
        'projects': [{'project_id': p.id, 'project_name': p.name, 'project_type': p.project_type} for p in user.projects]
    }
    return jsonify(user_info), 200

# Delete a user by username
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Create a new project
def create_project(request):
    data = request.json
    if not data or 'username' not in data or 'project_type' not in data or 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    project = Project(user_id=user.id, project_type=data['project_type'], name=data['name'])
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully', 'project_id': project.id}), 201

# Delete a project
def delete_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

# Upload an image to a project
def upload_image(project_id, request):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file or no file selected'}), 400
    filename = secure_filename(file.filename)
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    image = Image(filename=filename, label=request.form.get('label', ''), project_id=project.id)
    db.session.add(image)
    db.session.commit()
    return jsonify({'message': 'Image uploaded successfully', 'filename': filename}), 201

# Get information about an image
def get_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    image_info = {
        'image_id': image.id,
        'filename': image.filename,
        'label': image.label,
        'project_id': image.project_id,
        'project_name': image.project.name,
        'user_id': image.project.user_id,
        'associated_user': image.project.user.username
    }
    return jsonify(image_info), 200

# Delete an image
def delete_image(username, project_id, image_id):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    project = Project.query.filter_by(id=project_id, user_id=user.id).first()
    if not project:
        return jsonify({'error': 'Project not found or does not belong to the specified user'}), 404

    image = Image.query.filter_by(id=image_id, project_id=project.id).first()
    if not image:
        return jsonify({'error': 'Image not found or does not belong to the specified project'}), 404

    try:
        UPLOAD_FOLDER = 'uploads'
        filename = image.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)  # Delete the file from the filesystem
        db.session.delete(image)  # Delete the database record
        db.session.commit()
        return jsonify({'message': 'Image deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ANALYZE data
def analyze_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    images = Image.query.filter_by(project_id=project_id).all()
    
    if not images:
        return jsonify({'message': 'No images found for this project'}), 404
    
    # Extract feature sizes
    feature_sizes = [image.feature_size for image in images if image.feature_size is not None]
    
    if not feature_sizes:
        return jsonify({'message': 'No feature sizes available for images in this project'}), 404
    
    total_size = sum(feature_sizes)
    avg_size = total_size / len(feature_sizes)
    min_size = min(feature_sizes)
    max_size = max(feature_sizes)
    
    analysis_result = {
        'project_id': project_id,
        'num_images': len(images),
        'total_feature_size': total_size,
        'average_feature_size': avg_size,
        'smallest_image_size': min_size,
        'largest_image_size': max_size,
    }
    
    return jsonify(analysis_result), 200

# POST training configs
def configure_training(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.json
    if not data or 'learning_rate' not in data or 'epochs' not in data or 'batch_size' not in data:
        return jsonify({'error': 'Missing training parameters'}), 400
    
    if project.training_config:
        config = project.training_config
    else:
        config = TrainingConfig(project_id=project_id)
        db.session.add(config)
    
    config.learning_rate = data['learning_rate']
    config.epochs = data['epochs']
    config.batch_size = data['batch_size']
    db.session.commit()
    
    return jsonify({'message': 'Training configuration updated successfully'}), 200

# POST training queue
def enqueue_training(project_id):
    training_queue.put(project_id)
    return jsonify({'message': 'Training task enqueued'}), 202

# GET training results
def get_training_results(project_id):
    results = TrainingResult.query.filter_by(project_id=project_id).all()
    if not results:
        return jsonify({'error': 'No training results found'}), 404
    return jsonify([{'accuracy': r.accuracy, 'loss': r.loss, 'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S')} for r in results]), 200

# POST inference queue
def enqueue_inference(project_id, image_id):
    """Enqueues an inference task for a specific project and image."""
    # Simulate the inference task enqueueing
    inference_task = {'project_id': project_id, 'image_id': image_id}
    inference_queue.put(inference_task)
    return jsonify({'message': 'Inference task enqueued'}), 202

# GET inference results
def get_inference_results(image_id):
    result = InferenceResult.query.filter_by(image_id=image_id).first()
    if not result:
        return jsonify({'error': 'Inference result not found'}), 404
    return jsonify({
        'image_id': image_id,
        'prediction': result.result,
        'created_at': result.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

# Functions for image
def uploaded_file(filename):
    """Function to retrieve files from the upload directory."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
