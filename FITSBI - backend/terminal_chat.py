import requests

API_URL = "http://127.0.0.1:8000"

def get_token(email, password):
    response = requests.post(
        f"{API_URL}/token",
        data={"username": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Login failed:", response.json())
        return None

def get_user_id(token):
    # This assumes you have an endpoint to get current user info.
    # If not, you may need to modify this part.
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/users/me", headers=headers)
    if response.status_code == 200:
        return response.json()["_id"]
    else:
        print("Failed to get user info:", response.json())
        return None

def chat(user_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    print("Type 'exit' to quit.")
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break
        response = requests.post(
            f"{API_URL}/chat/{user_id}",
            params={"message": message},
            headers=headers
        )
        if response.status_code == 200:
            print("Bot:", response.json()["response"])
        else:
            print("Error:", response.json())

if __name__ == "__main__":
    email = input("Email: ")
    password = input("Password: ")
    token = get_token(email, password)
    if token:
        # You need to know your user_id. If you don't have a /users/me endpoint,
        # you can prompt for it or fetch it another way.
        user_id = input("Enter your user_id: ")
        chat(user_id, token)