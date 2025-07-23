from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId  # 🔥 ADDED: Import ObjectId for fixing update method
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL= "mongodb+srv://ashwin35t:Qi5rCPJexCGwnVAl@fitsbi.ihihoox.mongodb.net/fitness_ai?retryWrites=true&w=majority&appName=fitsbi"
DATABASE_NAME = "fitness_ai"

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None
    
    @classmethod
    async def connect_to_database(cls):
        print(f"🔍 DEBUG: Connecting with URL = {MONGODB_URL}")
        cls.client = AsyncIOMotorClient(
            MONGODB_URL,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        cls.db = cls.client[DATABASE_NAME]
        print("Connected to MongoDB!")
    
    @classmethod
    async def close_database_connection(cls):
        cls.client.close()
        print("Closed MongoDB connection!")
    
    @classmethod
    async def get_collection(cls, collection_name: str):
        return cls.db[collection_name]
    
    @classmethod
    def serialize_document(cls, doc):
        """Convert MongoDB document to JSON-serializable format"""
        if doc is None:
            return None
        
        if isinstance(doc, list):
            return [cls.serialize_document(item) for item in doc]
        
        if isinstance(doc, dict):
            serialized = {}
            for key, value in doc.items():
                if hasattr(value, '__class__') and 'ObjectId' in str(type(value)):
                    serialized[key] = str(value)
                elif isinstance(value, (dict, list)):
                    serialized[key] = cls.serialize_document(value)
                else:
                    serialized[key] = value
            return serialized
        
        return doc
    
    # ============ USER OPERATIONS ============
    @classmethod
    async def create_user(cls, user_data: dict):
        collection = await cls.get_collection("users")
        user_data['profile_completion'] = 0.0
        user_data['onboarding_completed'] = False
        user_data['last_profile_update'] = datetime.utcnow()
        result = await collection.insert_one(user_data)
        return result.inserted_id
    
    @classmethod
    async def get_user(cls, user_id: str):
        collection = await cls.get_collection("users")
        print(f"🔍 DEBUG: Looking for user_id: {user_id}")
        
        try:
            async for user in collection.find():
                user_obj_id = str(user.get("_id", ""))
                if user_obj_id == user_id:
                    print(f"✅ Found user by manual search")
                    return cls.serialize_document(user)
        except Exception as e:
            print(f"❌ Error in manual search: {e}")
        
        print(f"❌ User not found: {user_id}")
        return None
    
    @classmethod
    async def get_user_by_email(cls, email: str):
        collection = await cls.get_collection("users")
        user = await collection.find_one({"email": email})
        return cls.serialize_document(user)
    
    @classmethod
    async def update_user_profile(cls, user_id: str, update_data: Dict[str, Any]):
        """Update user profile with new data and calculate completion percentage"""
        collection = await cls.get_collection("users")
        
        print(f"🔍 DEBUG: Updating profile for user_id: {user_id}")
        print(f"🔍 DEBUG: Update data: {update_data}")
        
        # Add timestamp for last update
        update_data['last_profile_update'] = datetime.utcnow()
        
        # Calculate profile completion percentage
        user = await cls.get_user(user_id)
        if user:
            total_fields = [
                'age', 'gender', 'weight', 'height', 'location', 'fitness_goals',
                'activity_level', 'workout_frequency', 'sleep_hours', 'occupation',
                'medical_conditions', 'dietary_restrictions', 'stress_level',
                'available_equipment', 'preferred_workout_time'
            ]
            
            completed_fields = 0
            user_data = {**user, **update_data}
            
            for field in total_fields:
                if field in user_data and user_data[field] is not None:
                    if isinstance(user_data[field], list) and len(user_data[field]) > 0:
                        completed_fields += 1
                    elif not isinstance(user_data[field], list):
                        completed_fields += 1
            
            completion_percentage = (completed_fields / len(total_fields)) * 100
            update_data['profile_completion'] = completion_percentage
            
            if completion_percentage >= 80:
                update_data['onboarding_completed'] = True
        
        # 🔥 FIX: Convert string user_id back to ObjectId for MongoDB query
        try:
            object_id = ObjectId(user_id)
            result = await collection.update_one(
                {"_id": object_id},  # ← Fixed: Use ObjectId instead of string
                {"$set": update_data}
            )
            
            print(f"🔍 DEBUG: Update result - matched: {result.matched_count}, modified: {result.modified_count}")
            
            if result.matched_count == 0:
                print(f"❌ No user found with ObjectId: {object_id}")
                return False
                
            return result.modified_count > 0
            
        except Exception as e:
            print(f"❌ Error updating user profile: {e}")
            return False
    
    @classmethod
    async def get_incomplete_profile_fields(cls, user_id: str) -> List[str]:
        """Get list of incomplete profile fields for data collection"""
        user = await cls.get_user(user_id)
        if not user:
            return []
        
        required_fields = {
            'age': 'your age',
            'gender': 'your gender',
            'weight': 'your current weight',
            'height': 'your height',
            'location': 'your location',
            'fitness_goals': 'your fitness goals',
            'activity_level': 'your current activity level',
            'workout_frequency': 'how often you want to work out',
            'sleep_hours': 'how many hours you sleep',
            'occupation': 'your occupation',
            'stress_level': 'your stress level'
        }
        
        incomplete_fields = []
        for field, description in required_fields.items():
            if field not in user or user[field] is None or (isinstance(user[field], list) and len(user[field]) == 0):
                incomplete_fields.append(description)
        
        return incomplete_fields
    
    # ============ CHAT OPERATIONS ============
    @classmethod
    async def save_chat_message(cls, user_id: str, message: dict):
        collection = await cls.get_collection("chat_history")
        message["user_id"] = user_id
        message["timestamp"] = datetime.utcnow()
        result = await collection.insert_one(message)
        return result.inserted_id
    
    @classmethod
    async def get_user_chat_history(cls, user_id: str, limit: int = 50, days_back: int = None):
        collection = await cls.get_collection("chat_history")
        
        query = {"user_id": user_id}
        if days_back:
            start_date = datetime.utcnow() - timedelta(days=days_back)
            query["timestamp"] = {"$gte": start_date}
        
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        messages = await cursor.to_list(length=limit)
        
        # FIXED: Convert ObjectId to string for JSON serialization
        serialized_messages = cls.serialize_document(messages)
        
        return list(reversed(serialized_messages))  # Return in chronological order
    
    @classmethod
    async def get_today_chat_history(cls, user_id: str):
        """Get today's chat history for daily summary creation"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timedelta(days=1)
        
        collection = await cls.get_collection("chat_history")
        cursor = collection.find({
            "user_id": user_id,
            "timestamp": {
                "$gte": today_start,
                "$lt": tomorrow_start
            }
        }).sort("timestamp", 1)
        
        messages = await cursor.to_list(length=None)
        return cls.serialize_document(messages)
    
    # ============ DAILY SUMMARY OPERATIONS ============
    @classmethod
    async def save_daily_summary(cls, user_id: str, summary_data: dict):
        collection = await cls.get_collection("daily_summaries")
        summary_data["user_id"] = user_id
        summary_data["created_at"] = datetime.utcnow()
        
        # Upsert - update if exists for this date, create if not
        result = await collection.update_one(
            {
                "user_id": user_id,
                "date": summary_data["date"]
            },
            {"$set": summary_data},
            upsert=True
        )
        return result.upserted_id or True
    
    @classmethod
    async def get_recent_daily_summaries(cls, user_id: str, days: int = 7):
        collection = await cls.get_collection("daily_summaries")
        start_date = datetime.utcnow() - timedelta(days=days)
        
        cursor = collection.find({
            "user_id": user_id,
            "date": {"$gte": start_date}
        }).sort("date", -1)
        
        summaries = await cursor.to_list(length=days)
        return cls.serialize_document(summaries)
    
    @classmethod
    async def get_daily_summary(cls, user_id: str, date: datetime):
        collection = await cls.get_collection("daily_summaries")
        target_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        summary = await collection.find_one({
            "user_id": user_id,
            "date": target_date
        })
        return cls.serialize_document(summary)
    
    # ============ USER SUMMARY OPERATIONS ============
    @classmethod
    async def save_user_summary(cls, user_id: str, summary_data: dict):
        collection = await cls.get_collection("user_summaries")
        summary_data["user_id"] = user_id
        summary_data["last_updated"] = datetime.utcnow()
        
        # Increment version number
        existing = await collection.find_one({"user_id": user_id})
        if existing:
            summary_data["summary_version"] = existing.get("summary_version", 1) + 1
            result = await collection.update_one(
                {"user_id": user_id},
                {"$set": summary_data}
            )
        else:
            summary_data["summary_version"] = 1
            result = await collection.insert_one(summary_data)
        
        return result
    
    @classmethod
    async def get_user_summary(cls, user_id: str):
        collection = await cls.get_collection("user_summaries")
        summary = await collection.find_one({"user_id": user_id})
        return cls.serialize_document(summary)
    
    # ============ PROGRESS OPERATIONS ============
    @classmethod
    async def save_daily_progress(cls, user_id: str, progress_data: dict):
        collection = await cls.get_collection("daily_progress")
        progress_data["user_id"] = user_id
        progress_data["date"] = datetime.utcnow().date()
        result = await collection.insert_one(progress_data)
        return result.inserted_id
    
    @classmethod
    async def get_user_progress(cls, user_id: str, start_date: datetime, end_date: datetime):
        collection = await cls.get_collection("daily_progress")
        cursor = collection.find({
            "user_id": user_id,
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).sort("date", 1)
        
        progress = await cursor.to_list(length=None)
        return cls.serialize_document(progress)
    
    # ============ ANALYTICS & INSIGHTS ============
    @classmethod
    async def get_user_conversation_stats(cls, user_id: str, days: int = 30):
        """Get conversation statistics for analytics"""
        collection = await cls.get_collection("chat_history")
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "timestamp": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$timestamp"
                        }
                    },
                    "message_count": {"$sum": 1},
                    "user_messages": {
                        "$sum": {
                            "$cond": [{"$eq": ["$role", "user"]}, 1, 0]
                        }
                    }
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        cursor = collection.aggregate(pipeline)
        stats = await cursor.to_list(length=None)
        return cls.serialize_document(stats)