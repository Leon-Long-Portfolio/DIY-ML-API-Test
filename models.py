from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Model
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', backref='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    images = db.relationship('Image', backref='project', lazy=True)
    training_config = db.relationship('TrainingConfig', uselist=False, back_populates='project')

# Image Model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=True)
    feature_size = db.Column(db.Float, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)

# Training Configurations Model
class TrainingConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    learning_rate = db.Column(db.Float, nullable=False, default=0.001)
    epochs = db.Column(db.Integer, nullable=False, default=10)
    batch_size = db.Column(db.Integer, nullable=False, default=32)
    project = db.relationship('Project', back_populates='training_config')

# Training Result Model
class TrainingResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    accuracy = db.Column(db.Float)
    loss = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Inference Result Model
class InferenceResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    result = db.Column(db.String(256))  # Placeholder for inference result
    created_at = db.Column(db.DateTime, default=datetime.utcnow)