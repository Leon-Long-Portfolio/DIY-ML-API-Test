from flask import Blueprint, request, jsonify
import services

api = Blueprint('api', __name__)

@api.route('/register/', methods=['POST'])
def register():
    return services.register_user(request)

@api.route('/user/<username>/', methods=['GET'])
def get_user(username):
    return services.get_user(username)

@api.route('/delete_user/<username>/', methods=['DELETE'])
def delete_user(username):
    return services.delete_user(username)

@api.route('/create_project/', methods=['POST'])
def create_project():
    return services.create_project(request)

@api.route('/project/<int:project_id>/', methods=['GET'])
def get_project(project_id):
    return services.get_project(project_id)

@api.route('/delete_project/<int:project_id>/', methods=['DELETE'])
def delete_project(project_id):
    return services.delete_project(project_id)

@api.route('/upload_image/<int:project_id>/', methods=['POST'])
def upload_image(project_id):
    return services.upload_image(project_id, request)

@api.route('/image/<int:image_id>/', methods=['GET'])
def get_image(image_id):
    return services.get_image(image_id)

@api.route('/delete_image/<username>/<int:project_id>/<int:image_id>/', methods=['DELETE'])
def delete_image(username, project_id, image_id):
    return services.delete_image(username, project_id, image_id)

@api.route('/analyze_project/<int:project_id>/', methods=['GET'])
def analyze_project(project_id):
    return services.analyze_project(project_id)

@api.route('/configure_training/<int:project_id>/', methods=['POST'])
def configure_training(project_id):
    return services.configure_training(project_id, request)

@api.route('/enqueue_training/<int:project_id>/', methods=['POST'])
def enqueue_training(project_id):
    return services.enqueue_training(project_id)

@api.route('/training_results/<int:project_id>/', methods=['GET'])
def get_training_results(project_id):
    return services.get_training_results(project_id)

@api.route('/enqueue_inference/<int:project_id>/<int:image_id>/', methods=['POST'])
def enqueue_inference(project_id, image_id):
    return services.enqueue_inference(project_id, image_id)

@api.route('/inference_results/<int:image_id>/', methods=['GET'])
def get_inference_results(image_id):
    return services.get_inference_results(image_id)

@api.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return services.uploaded_file(filename)
