from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration for the Flask application to connect to an SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Method to hash the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to verify the password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Project model definition
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    user = db.relationship('User', backref=db.backref('projects', lazy=True, cascade="all, delete"))

# Database initialization function
def setup_database(app):
    with app.app_context():
        db.create_all()

# Endpoint to register a new user
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

# Endpoint to get user data
@app.route('/user/<username>/', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    projects = [{
        'project_id': project.id,
        'project_name': project.name,
        'project_type': project.project_type
    } for project in user.projects]

    user_info = {
        'username': user.username,
        'user_id': user.id,
        'projects': projects
    }
    return jsonify(user_info), 200

# Endpoint to delete a user
@app.route('/delete_user/<username>/', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Endpoint to create a new project
@app.route('/create_project/', methods=['POST'])
def create_project():
    data = request.json
    if not data or 'username' not in data or 'project_type' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    name = data.get('name', 'Unnamed Project')
    
    new_project = Project(user_id=user.id, project_type=data['project_type'], name=name)
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'message': 'Project created successfully', 'project_id': new_project.id}), 201

# Endpoint to get project data
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

# Endpoint to delete a project
@app.route('/delete_project/', methods=['DELETE'])
def delete_project():
    project_identifier = request.args.get('identifier')
    if not project_identifier:
        return jsonify({'error': 'Project identifier required'}), 400

    project = Project.query.filter((Project.id == project_identifier) | (Project.name == project_identifier)).first()
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

if __name__ == '__main__':
    setup_database(app)
    app.run(debug=True, port=8000)
