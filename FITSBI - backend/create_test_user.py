import asyncio
from mongodb import MongoDB

async def create_test_user():
    await MongoDB.connect_to_database()
    
    user_data = {
        "email": "alfi@example.com",
        "name": "Alfi",
        "age": 25,
        "weight": 70,
        "height": 175,
        "fitness_goals": ["weight_loss"],
        "medical_conditions": [],
        "injuries": [],
        "dietary_restrictions": [],
        "password": "passPASS12?"  # Plain text for now
    }
    
    result = await MongoDB.create_user(user_data)
    print(f"User created with ID: {result}")
    
    await MongoDB.close_database_connection()

if __name__ == "__main__":
    asyncio.run(create_test_user())