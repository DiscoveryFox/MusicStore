import requests
import random
import string

# Define the base URL of your Flask application
base_url = "http://localhost:5000"  # Change this to your application's URL


# Generate a random username, email, and password
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


random_username = generate_random_string(8)
random_email = generate_random_string(8) + "@example.com"
random_password = generate_random_string(12)

# Create a random user
user_data = {
    "full_name": "Random User",
    "username": random_username,
    "email": random_email,
    "password": random_password,
}

registration_url = base_url + "/register"  # Replace with your registration endpoint URL

# Send a POST request to register the user
response = requests.post(registration_url, data=user_data)

if response.status_code == 200:
    print("User registration successful.")
    print(f"Username: {random_username}")
    print(f"Email: {random_email}")
    print(f"Password: {random_password}")
else:
    print("User registration failed.")
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
