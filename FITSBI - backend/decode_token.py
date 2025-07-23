import requests
import jwt

API_URL = "http://127.0.0.1:8000"

def get_token_and_user_id(email, password):
    """Login and return both token and user_id"""
    response = requests.post(
        f"{API_URL}/token",
        data={"username": email, "password": password}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        
        # Decode token to get user_id
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get("sub")
            return token, user_id
        except Exception as e:
            print(f"Error decoding token: {e}")
            return token, None
    else:
        print(f"Login failed. Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None, None

def chat_with_ai(token, user_id, message):
    """Send message to AI and get response"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"message": message}
    
    response = requests.post(
        f"{API_URL}/chat/{user_id}",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        try:
            error_detail = response.json()
            return f"Error: {error_detail}"
        except:
            return f"Error {response.status_code}: {response.text}"

def main():
    print("🏋️ Welcome to Fitness AI Chat!")
    print("=" * 40)
    
    # Login
    email = input("Email: ")
    password = input("Password: ")
    
    print("🔐 Logging in...")
    token, user_id = get_token_and_user_id(email, password)
    
    if not token or not user_id:
        print("❌ Failed to login or get user ID")
        return
    
    print(f"✅ Login successful!")
    print(f"👤 Your User ID: {user_id}")
    print("💬 Chat started! Type 'exit' to quit.")
    print("=" * 40)
    
    # Chat loop
    while True:
        message = input("\nYou: ")
        if message.lower() in ['exit', 'quit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if message.strip() == "":
            continue
        
        print("🤖 AI is thinking...")
        response = chat_with_ai(token, user_id, message)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()