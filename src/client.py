import requests

# Function to interpret server response
def handle_response(response):
    try:
        print("Response:", response.json())
    except ValueError:  # Includes simplejson.decoder.JSONDecodeError
        print("Operation completed successfully, but no data returned.")

# Registers new user
def register_user():
    url = "http://localhost:8000/register/"
    user_data = {
        "username": input("Enter Username: "),
        "password": input("Enter Password: ")
    }
    response = requests.post(url, json=user_data)
    handle_response(response)

# Get user information
def get_user():
    username = input("Enter Username: ")
    url = f"http://localhost:8000/user/{username}/"
    response = requests.get(url)
    handle_response(response)

# Delete user
def delete_user():
    username = input("Enter Username to delete: ")
    url = f"http://localhost:8000/delete_user/{username}/"
    response = requests.delete(url)
    handle_response(response)

# Create new project
def create_project():
    url = "http://localhost:8000/create_project/"
    project_data = {
        "username": input("Enter Username: "),
        "project_type": input("Enter Project Type (1. Image Classification or 2. Object Detection): "),
        "name": input("Enter Project Name (optional, press Enter to skip): ")
    }
    response = requests.post(url, json=project_data)
    handle_response(response)

# Get project information
def get_project():
    project_id = input("Enter Project ID: ")
    url = f"http://localhost:8000/project/{project_id}/"
    response = requests.get(url)
    handle_response(response)

# Delete project
def delete_project():
    identifier = input("Enter Project ID or Name to delete: ")
    url = f"http://localhost:8000/delete_project/?identifier={identifier}"
    response = requests.delete(url)
    handle_response(response)

# Upload image
def upload_image():
    project_id = input("Enter Project ID for image upload: ")
    url = f"http://localhost:8000/upload_image/{project_id}/"
    filename = input("Enter filename of the image to upload: ")
    files = {'file': open(filename, 'rb')}
    label = input("Enter label for the image (optional): ")
    data = {'label': label}
    response = requests.post(url, files=files, data=data)
    handle_response(response)

# Get image infromation
def get_image():
    image_id = input("Enter Image ID: ")
    url = f"http://localhost:8000/image/{image_id}/"
    response = requests.get(url)
    handle_response(response)

# Delete image
def delete_image():
    username = input("Enter Username: ")
    project_id = input("Enter Project ID: ")
    image_id = input("Enter Image ID to delete: ")
    url = f"http://localhost:8000/delete_image/{username}/{project_id}/{image_id}/"
    response = requests.delete(url)
    handle_response(response)

# Analyze project
def analyze_project():
    project_id = input("Enter Project ID for analysis: ")
    url = f"http://localhost:8000/analyze_project/{project_id}/"
    response = requests.get(url)
    handle_response(response)

# Configure training
def configure_training():
    project_id = input("Enter Project ID to configure training: ")
    url = f"http://localhost:8000/configure_training/{project_id}/"
    config_data = {
        "learning_rate": float(input("Enter learning rate: ")),
        "epochs": int(input("Enter number of epochs: ")),
        "batch_size": int(input("Enter batch size: "))
    }
    response = requests.post(url, json=config_data)
    handle_response(response)

# Enqueue training
def enqueue_training():
    project_id = input("Enter Project ID to enqueue for training: ")
    url = f"http://localhost:8000/enqueue_training/{project_id}/"
    response = requests.post(url)
    handle_response(response)

# Get training results
def get_training_results():
    project_id = input("Enter Project ID to get training results: ")
    url = f"http://localhost:8000/training_results/{project_id}/" 
    response = requests.get(url)
    handle_response(response)

# Enqueue inference
def enqueue_inference():
    project_id = input("Enter Project ID for inference: ")
    image_id = input("Enter Image ID for inference: ")
    url = f"http://localhost:8000/enqueue_inference/{project_id}/{image_id}/"
    response = requests.post(url)
    handle_response(response)

# Get inference results
def get_inference_results():
    image_id = input("Enter Image ID to get inference results: ")
    url = f"http://localhost:8000/inference_results/{image_id}/"
    response = requests.get(url)
    handle_response(response)

def main():
    actions = {
        '1': register_user,
        '2': get_user,
        '3': delete_user,
        '4': create_project,
        '5': get_project,
        '6': delete_project,
        '7': upload_image,
        '8': get_image,
        '9': delete_image,
        '10': analyze_project,
        '11': configure_training,
        '12': enqueue_training,
        '13': get_training_results,
        '14': enqueue_inference,
        '15': get_inference_results,
        '16': exit
    }
    while True:
        choice = input("\nEnter number: \n"
                       "1. Register User\n"
                       "2. Get User Info\n"
                       "3. Delete User\n"
                       "4. Create Project\n"
                       "5. Get Project Info\n"
                       "6. Delete Project\n"
                       "7. Upload Image\n"
                       "8. Get Image Info\n"
                       "9. Delete Image\n"
                       "10. Analyze Project\n"
                       "11. Configure Training\n"
                       "12. Enqueue Training\n"
                       "13. Get Training Results\n"
                       "14. Enqueue Inference\n"
                       "15. Get Inference Results\n" 
                       "16. Quit\n"
                       "Your choice: ")
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Unknown option, please enter a valid number.")

if __name__ == '__main__':
    main()
