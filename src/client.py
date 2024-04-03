import requests

def handle_response(response):
    try:
        print("Response:", response.json())
    except ValueError:
        print("Operation completed successfully, but no data returned.")

def register_user():
    url = "http://localhost:8000/register/"
    user_data = {
        "username": input("Enter Username: "),
        "password": input("Enter Password: ")
    }
    response = requests.post(url, json=user_data)
    handle_response(response)

def get_user():
    username = input("Enter Username: ")
    url = f"http://localhost:8000/user/{username}/"
    response = requests.get(url)
    handle_response(response)

def delete_user():
    username = input("Enter Username to delete: ")
    url = f"http://localhost:8000/delete_user/{username}/"
    response = requests.delete(url)
    handle_response(response)

def create_project():
    url = "http://localhost:8000/create_project/"
    project_data = {
        "username": input("Enter Username: "),
        "project_type": input("Enter Project Type (1. Image Classification or 2. Object Detection): "),
        "name": input("Enter Project Name (optional, press Enter to skip): ")
    }
    response = requests.post(url, json=project_data)
    handle_response(response)

def get_project():
    project_id = input("Enter Project ID: ")
    url = f"http://localhost:8000/project/{project_id}/"
    response = requests.get(url)
    handle_response(response)

def delete_project():
    identifier = input("Enter Project ID or Name to delete: ")
    url = f"http://localhost:8000/delete_project/?identifier={identifier}"
    response = requests.delete(url)
    handle_response(response)

def upload_image():
    project_id = input("Enter Project ID for image upload: ")
    url = f"http://localhost:8000/upload_image/{project_id}/"
    filename = input("Enter filename of the image to upload: ")
    files = {'file': open(filename, 'rb')}
    label = input("Enter label for the image (optional): ")
    data = {'label': label}
    response = requests.post(url, files=files, data=data)
    handle_response(response)

def get_image():
    image_id = input("Enter Image ID: ")
    url = f"http://localhost:8000/image/{image_id}/"
    response = requests.get(url)
    handle_response(response)

def delete_image():
    image_id = input("Enter Image ID to delete: ")
    url = f"http://localhost:8000/delete_image/{image_id}/"
    response = requests.delete(url)
    handle_response(response)

def analyze_project():
    project_id = input("Enter Project ID for analysis: ")
    url = f"http://localhost:8000/analyze_project/{project_id}/"
    response = requests.get(url)
    handle_response(response)

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

def main():
    actions = {
        '1': register_user,
        '2': create_project,
        '3': get_user,
        '4': get_project,
        '5': delete_user,
        '6': delete_project,
        '7': upload_image,
        '8': get_image,
        '9': delete_image,
        '10': analyze_project,
        '11': configure_training,
        '12': exit
    }
    while True:
        choice = input("\nEnter number: \n1. Register User\n2. Create Project\n3. Get User Info\n4. Get Project Info\n5. Delete User\n6. Delete Project\n7. Upload Image\n8. Get Image Info\n9. Delete Image\n10. Analyze Project\n11. Configure Training\n12. Quit\n")
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Unknown option, please enter a valid number.")

if __name__ == '__main__':
    main()
