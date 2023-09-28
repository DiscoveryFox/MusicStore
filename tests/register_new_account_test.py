import requests
from faker import Faker

# Define the base URL of your Flask application
base_url = "http://localhost:5000"  # Change this to your application's URL

# Initialize Faker
fake = Faker()


# Generate a random user data
def generate_random_user_data():
    username = fake.user_name()
    email = fake.email()
    password = fake.password(length=12)
    full_name = fake.name()
    return {
        "full_name": full_name,
        "username": username,
        "email": email,
        "password": password,
    }


# Register a random user
def register_random_user():
    user_data = generate_random_user_data()
    registration_url = (
        f"{base_url}/register"  # Replace with your registration endpoint URL
    )

    # Send a POST request to register the user
    response = requests.post(registration_url, data=user_data)

    if response.status_code == 200:
        print("User registration successful.")
        for key, value in user_data.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("User registration failed.")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)


if __name__ == "__main__":
    register_random_user()
