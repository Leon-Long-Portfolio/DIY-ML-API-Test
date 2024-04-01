import requests

base_url = "http://localhost:8000"

def register_user():
    url = f"{base_url}/register/"
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    user_data = {"username": username, "password": password}
    try:
        response = requests.post(url, json=user_data)
        print("Response:", response.json())
    except Exception as e:
        print(f"ERROR: Failed to register user. Error: {e}")

def get_user():
    username = input("Enter Username: ")
    url = f"{base_url}/user/{username}/"
    try:
        response = requests.get(url)
        if response.ok:
            user_info = response.json()
            print("Username:", user_info['username'])
            print("User ID:", user_info['user_id'])
            print("Projects:")
            for project in user_info.get('projects', []):
                print(f"\tProject ID: {project['project_id']}, Name: {project['project_name']}, Type: {project['project_type']}")
        else:
            print("Error:", response.json())
    except Exception as e:
        print(f"ERROR: Failed to get user. Error: {e}")

def delete_user():
    username = input("Enter Username to delete: ")
    url = f"{base_url}/delete_user/{username}/"
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            print("User deleted successfully.")
        else:
            print("Response:", response.json())
    except Exception as e:
        print(f"ERROR: Failed to delete user. Error: {e}")

def create_project():
    url = f"{base_url}/create_project/"
    username = input("Enter Username: ")
    project_type = input("Enter Project Type (1. Image Classification or 2. Object Detection): ")
    project_type = "Image Classification" if project_type == '1' else "Object Detection"
    name = input("Enter Project Name (optional, press Enter to skip): ")
    project_data = {"username": username, "project_type": project_type, "name": name}
    try:
        response = requests.post(url, json=project_data)
        print("Response:", response.json())
    except Exception as e:
        print(f"ERROR: Failed to create project. Error: {e}")

def get_project():
    project_id = input("Enter Project ID: ")
    url = f"{base_url}/project/{project_id}/"
    try:
        response = requests.get(url)
        if response.ok:
            project_info = response.json()
            print("Project ID:", project_info['project_id'])
            print("Project Name:", project_info['project_name'])
            print("Project Type:", project_info['project_type'])
            print("Associated User ID:", project_info['user_id'])
            print("Associated Username:", project_info['associated_user'])
        else:
            print("Error:", response.json())
    except Exception as e:
        print(f"ERROR: Failed to get project. Error: {e}")

def delete_project():
    identifier = input("Enter Project ID or Name to delete: ")
    url = f"{base_url}/delete_project/?identifier={identifier}"
    try:
        response = requests.delete(url)
        if response.ok:
            print("Project deleted successfully.")
        else:
            print("Response:", response.json())
    except Exception as e:
        print(f"ERROR: Failed to delete project. Error: {e}")

def main():
    actions = {
        '1': register_user,
        '2': create_project,
        '3': get_user,
        '4': get_project,
        '5': delete_user,
        '6': delete_project,
        '7': quit
    }
    while True:
        inp = input("\nEnter number: \n\t1. Register User \n\t2. Create Project \n\t3. Get User Info\n\t4. Get Project Info\n\t5. Delete User\n\t6. Delete Project\n\t7. Quit\n")
        action = actions.get(inp)
        if action:
            action()
        else:
            print("Unknown option, please enter a valid number.")

if __name__ == '__main__':
    main()
