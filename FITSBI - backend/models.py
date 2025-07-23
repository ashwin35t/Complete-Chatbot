from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class FitnessGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    ENDURANCE = "endurance"
    FLEXIBILITY = "flexibility"
    GENERAL_FITNESS = "general_fitness"
    STRENGTH = "strength"
    CARDIO_HEALTH = "cardio_health"
    STRESS_MANAGEMENT = "stress_management"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

class SleepQuality(str, Enum):
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class StressLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

class UserBase(BaseModel):
    email: str
    name: str
    # Basic Demographics
    age: Optional[int] = None
    gender: Optional[Gender] = None
    weight: Optional[float] = None  # in kg
    height: Optional[float] = None  # in cm
    
    # Location & Environment
    location: Optional[str] = None  # city, country
    timezone: Optional[str] = None
    climate: Optional[str] = None  # tropical, temperate, cold, etc.
    
    # Fitness & Health Goals
    fitness_goals: Optional[List[FitnessGoal]] = []
    target_weight: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    workout_frequency: Optional[int] = None  # times per week
    preferred_workout_duration: Optional[int] = None  # minutes
    preferred_workout_time: Optional[str] = None  # morning, afternoon, evening
    
    # Health Conditions & Limitations
    medical_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    injuries: Optional[List[str]] = []
    physical_limitations: Optional[List[str]] = []
    mental_health_conditions: Optional[List[str]] = []
    
    # Lifestyle & Sleep
    sleep_hours: Optional[float] = None  # average hours per night
    sleep_quality: Optional[SleepQuality] = None
    bedtime: Optional[str] = None  # e.g., "23:00"
    wake_time: Optional[str] = None  # e.g., "07:00"
    
    # Diet & Nutrition
    dietary_restrictions: Optional[List[str]] = []
    food_allergies: Optional[List[str]] = []
    preferred_diet_type: Optional[str] = None  # vegetarian, vegan, keto, etc.
    daily_water_goal: Optional[float] = None  # liters
    
    # Work & Stress
    occupation: Optional[str] = None
    work_schedule: Optional[str] = None  # 9-5, night shift, flexible, etc.
    stress_level: Optional[StressLevel] = None
    stress_factors: Optional[List[str]] = []
    
    # Equipment & Preferences
    available_equipment: Optional[List[str]] = []
    gym_access: Optional[bool] = None
    home_workout_space: Optional[bool] = None
    budget_for_fitness: Optional[str] = None  # low, medium, high
    
    # Data Collection Progress
    profile_completion: Optional[float] = 0.0  # percentage of profile completed
    last_profile_update: Optional[datetime] = None
    onboarding_completed: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime
    last_login: datetime
    provider: Optional[str] = "email"  # email, google, etc.

class ChatMessage(BaseModel):
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_type: Optional[str] = "chat"  # chat, data_collection, summary
    extracted_data: Optional[Dict[str, Any]] = {}  # any user data extracted from message

class DailyProgress(BaseModel):
    user_id: str
    date: datetime
    weight: Optional[float]
    calories_consumed: Optional[int]
    calories_burned: Optional[int]
    workout_duration: Optional[int]  # in minutes
    workout_type: Optional[str]
    steps: Optional[int]
    water_intake: Optional[float]  # in liters
    sleep_hours: Optional[float]
    sleep_quality: Optional[SleepQuality]
    mood: Optional[str]
    stress_level: Optional[StressLevel]
    energy_level: Optional[int]  # 1-10 scale
    notes: Optional[str]

class DailySummary(BaseModel):
    user_id: str
    date: datetime
    summary_text: str  # AI-generated summary of the day
    key_activities: List[str]
    mood_trends: Optional[str]
    health_insights: Optional[str]
    progress_notes: Optional[str]
    conversation_count: int
    data_updates: Dict[str, Any]  # any profile updates made that day
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserSummary(BaseModel):
    user_id: str
    overall_summary: str  # comprehensive summary of user's journey
    recent_patterns: str  # patterns from last 7-14 days
    health_trends: str  # long-term health trends
    goals_progress: str  # progress towards fitness goals
    recommendations: str  # current recommendations
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    summary_version: int = 1  # increments each time summary is updated

class WorkoutPlan(BaseModel):
    user_id: str
    created_at: datetime
    exercises: List[dict]
    duration: int  # in minutes
    difficulty: str
    target_muscle_groups: List[str]
    equipment_needed: List[str]
    personalization_notes: Optional[str]

class DietPlan(BaseModel):
    user_id: str
    created_at: datetime
    meals: List[dict]
    total_calories: int
    macros: dict  # protein, carbs, fats
    dietary_restrictions: List[str]
    personalization_notes: Optional[str]

class DataCollectionTemplate(BaseModel):
    """Template for systematic data collection"""
    category: str  # demographics, health, lifestyle, preferences
    questions: List[str]
    priority: int  # 1-5, higher is more important
    dependencies: Optional[List[str]] = []  # other categories that should be collected first