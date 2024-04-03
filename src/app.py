from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

db = SQLAlchemy(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', backref='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    images = db.relationship('Image', backref='project', cascade="all, delete-orphan")
    training_config = db.relationship('TrainingConfig', uselist=False, back_populates='project')

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)

class TrainingConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    learning_rate = db.Column(db.Float, nullable=False, default=0.001)
    epochs = db.Column(db.Integer, nullable=False, default=10)
    batch_size = db.Column(db.Integer, nullable=False, default=32)
    project = db.relationship('Project', back_populates='training_config')

@app.route('/register/', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/user/<username>/', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_info = {
        'username': user.username,
        'user_id': user.id,
        'projects': [{
            'project_id': project.id,
            'project_name': project.name,
            'project_type': project.project_type
        } for project in user.projects]
    }
    return jsonify(user_info), 200

@app.route('/delete_user/<username>/', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/create_project/', methods=['POST'])
def create_project():
    data = request.json
    if not data or 'username' not in data or 'project_type' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    project = Project(user_id=user.id, project_type=data['project_type'], name=data.get('name', 'Unnamed Project'))
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully', 'project_id': project.id}), 201

@app.route('/project/<int:project_id>/', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    project_info = {
        'project_id': project.id,
        'project_name': project.name,
        'project_type': project.project_type,
        'user_id': project.user_id,
        'associated_user': project.user.username
    }
    return jsonify(project_info), 200

@app.route('/delete_project/', methods=['DELETE'])
def delete_project():
    project_identifier = request.args.get('identifier')
    project = Project.query.filter((Project.id == project_identifier) | (Project.name == project_identifier)).first()
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

# Upload image
@app.route('/upload_image/<int:project_id>/', methods=['POST'])
def upload_image(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file or no file selected'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    image = Image(filename=filename, label=request.form.get('label', ''), project_id=project.id)
    db.session.add(image)
    db.session.commit()
    return jsonify({'message': 'Image uploaded successfully', 'filename': filename}), 201

# GET image information
@app.route('/image/<int:image_id>/', methods=['GET'])
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

# Add this route to delete an image
@app.route('/delete_image/<int:image_id>/', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    filename = image.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(filepath)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'message': 'Image deleted successfully'}), 200

# GET analysis
@app.route('/analyze_project/<int:project_id>/', methods=['GET'])
def analyze_project(project_id):
    # Placeholder for analysis logic
    return jsonify({'message': 'Data analysis result', 'project_id': project_id}), 200

@app.route('/configure_training/<int:project_id>/', methods=['POST'])
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


# Add this route to serve images
@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Allowed file formats
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
