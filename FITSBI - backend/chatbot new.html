import openai
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import json
import re
from models import ChatMessage, User, DailyProgress, DailySummary
from mongodb import MongoDB

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class FitnessChatbot:
    def __init__(self):
        self.system_prompt = """You are Fitsbi — a chill, supportive gym buddy with Gen Z energy.

Speak like a hyped-up friend who's always down for a solid session.

Keep replies short — max 2–3 sentences, no lectures.

Use emojis where it feels right 💪🔥😄 — make it fun, not formal.

Drop casual, playful questions to collect info like fitness history, goals, height, age, or weight without directly asking.

Example: "You more tall-at-the-back-of-group-pics or middle-row energy?"

Or: "You on that bulk, shred, or just-vibin' phase right now?"

Slide in fitness experience checks naturally — "Been racking plates for years or still figuring out which way the dumbbell curls?"

Always ask (directly or sneakily) about joint pain or injuries before giving workout advice.

Example: "Knees, shoulders, anything acting up like it's Monday?"

If they mention pain/injury later, switch to safe/modified advice and say something like "All good — we'll go joint-friendly and still crush it 🙌."

Never act like a doctor — be careful and encouraging.

If something sounds serious, gently say: "Not tryna play doc here, maybe best to get that checked just in case."

Do casual mood or energy checks every now and then — "Mood scale: 1 to deadlifting your problems — where we at today?"

Use bullet points, short lists, or structured responses to keep things scrollable and fun to read.

Always be upbeat, real, and motivational — like a buddy who's got their back, not a coach with a whistle.

CONVERSATION STYLE:
- Be warm, supportive, and personal
- Ask one question at a time to avoid overwhelming
- Reference previous conversations naturally
- Acknowledge progress and changes
- Provide specific, actionable advice
- Use the user's name when appropriate"""

        self.data_collection_priorities = {
            1: ["age", "gender", "fitness_goals"],  # High priority - essential basics
            2: ["weight", "height", "activity_level"],  # Physical metrics
            3: ["workout_frequency", "sleep_hours", "stress_level"],  # Lifestyle basics
            4: ["medical_conditions", "injuries", "dietary_restrictions"],  # Health considerations
            5: ["location", "occupation", "available_equipment"]  # Environmental factors
        }

    async def _build_user_context(self, user_id: str) -> str:
        """Build comprehensive user context from profile, summaries, and recent history"""
        user = await MongoDB.get_user(user_id)
        if not user:
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."

    async def generate_workout_plan(self, user_id: str) -> Dict:
        """Generate a personalized workout plan"""
        context = await self._build_user_context(user_id)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"User Context:\n{context}"},
            {"role": "user", "content": "Please generate a detailed, personalized workout plan for me based on my profile, goals, and current fitness level."}
        ]

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4.1-nano",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            workout_plan = {
                "user_id": user_id,
                "created_at": datetime.utcnow(),
                "plan": response.choices[0].message.content,
                "personalization_notes": f"Generated based on user profile completion and current fitness level"
            }
            
            return workout_plan
            
        except Exception as e:
            print(f"Error generating workout plan: {str(e)}")
            return None

    async def generate_diet_plan(self, user_id: str) -> Dict:
        """Generate a personalized diet plan"""
        context = await self._build_user_context(user_id)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"User Context:\n{context}"},
            {"role": "user", "content": "Please generate a detailed, personalized nutrition plan for me based on my profile, goals, dietary restrictions, and lifestyle."}
        ]

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4.1-nano",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            diet_plan = {
                "user_id": user_id,
                "created_at": datetime.utcnow(),
                "plan": response.choices[0].message.content,
                "personalization_notes": f"Generated based on user dietary restrictions and fitness goals"
            }
            
            return diet_plan
            
        except Exception as e:
            print(f"Error generating diet plan: {str(e)}")
            return None 

        context = "=== USER PROFILE ===\n"
        
        # Basic Demographics
        if user.get('name'):
            context += f"Name: {user['name']}\n"
        if user.get('age'):
            context += f"Age: {user['age']}\n"
        if user.get('gender'):
            context += f"Gender: {user['gender']}\n"
        if user.get('location'):
            context += f"Location: {user['location']}\n"

        # Physical Metrics
        if user.get('height') or user.get('weight'):
            context += "\nPhysical Metrics:\n"
            if user.get('height'):
                context += f"Height: {user['height']}cm\n"
            if user.get('weight'):
                context += f"Weight: {user['weight']}kg\n"
            if user.get('target_weight'):
                context += f"Target Weight: {user['target_weight']}kg\n"

        # Fitness & Activity
        if user.get('fitness_goals'):
            context += f"\nFitness Goals: {', '.join(user['fitness_goals'])}\n"
        if user.get('activity_level'):
            context += f"Activity Level: {user['activity_level']}\n"
        if user.get('workout_frequency'):
            context += f"Workout Frequency: {user['workout_frequency']} times/week\n"

        # Health Considerations
        health_info = []
        if user.get('medical_conditions'):
            health_info.append(f"Medical Conditions: {', '.join(user['medical_conditions'])}")
        if user.get('injuries'):
            health_info.append(f"Injuries: {', '.join(user['injuries'])}")
        if user.get('medications'):
            health_info.append(f"Medications: {', '.join(user['medications'])}")
        if health_info:
            context += f"\nHealth Considerations:\n" + "\n".join(health_info) + "\n"

        # Lifestyle
        lifestyle_info = []
        if user.get('sleep_hours'):
            lifestyle_info.append(f"Sleep: {user['sleep_hours']} hours/night")
        if user.get('stress_level'):
            lifestyle_info.append(f"Stress Level: {user['stress_level']}")
        if user.get('occupation'):
            lifestyle_info.append(f"Occupation: {user['occupation']}")
        if lifestyle_info:
            context += f"\nLifestyle:\n" + "\n".join(lifestyle_info) + "\n"

        # Diet & Nutrition
        if user.get('dietary_restrictions') or user.get('food_allergies'):
            context += "\nNutrition:\n"
            if user.get('dietary_restrictions'):
                context += f"Dietary Restrictions: {', '.join(user['dietary_restrictions'])}\n"
            if user.get('food_allergies'):
                context += f"Food Allergies: {', '.join(user['food_allergies'])}\n"

        # Equipment & Preferences
        if user.get('available_equipment') or user.get('gym_access') is not None:
            context += "\nFitness Resources:\n"
            if user.get('available_equipment'):
                context += f"Equipment: {', '.join(user['available_equipment'])}\n"
            if user.get('gym_access') is not None:
                context += f"Gym Access: {'Yes' if user['gym_access'] else 'No'}\n"

        # Profile completion status
        completion = user.get('profile_completion', 0)
        context += f"\nProfile Completion: {completion:.0f}%\n"

        # Get user summary (long-term memory)
        user_summary = await MongoDB.get_user_summary(user_id)
        if user_summary:
            context += f"\n=== USER JOURNEY SUMMARY ===\n"
            context += f"{user_summary.get('overall_summary', '')}\n"
            if user_summary.get('recent_patterns'):
                context += f"\nRecent Patterns: {user_summary['recent_patterns']}\n"
            if user_summary.get('goals_progress'):
                context += f"Goals Progress: {user_summary['goals_progress']}\n"

        # Get recent daily summaries
        recent_summaries = await MongoDB.get_recent_daily_summaries(user_id, days=7)
        if recent_summaries:
            context += f"\n=== RECENT DAILY SUMMARIES ===\n"
            for summary in recent_summaries[-3:]:  # Last 3 days
                date_str = summary['date'].strftime('%Y-%m-%d')
                context += f"{date_str}: {summary['summary_text']}\n"

        return context

    async def _identify_missing_data(self, user_id: str) -> Optional[str]:
        """Identify the next most important piece of missing user data"""
        incomplete_fields = await MongoDB.get_incomplete_profile_fields(user_id)
        
        if not incomplete_fields:
            return None

        # Return a natural question for the highest priority missing field
        user = await MongoDB.get_user(user_id)
        profile_completion = user.get('profile_completion', 0)

        # Early stage questions (0-30% complete)
        if profile_completion < 30:
            if 'your age' in incomplete_fields:
                return "To give you the best personalized advice, could you tell me your age?"
            if 'your fitness goals' in incomplete_fields:
                return "What are your main fitness goals? For example, weight loss, muscle gain, general fitness, or something else?"
            if 'your current weight' in incomplete_fields:
                return "Could you share your current weight? This helps me calculate calorie needs and track progress."

        # Mid-stage questions (30-60% complete)
        elif profile_completion < 60:
            if 'your height' in incomplete_fields:
                return "What's your height? This helps me calculate your BMI and calorie requirements."
            if 'your current activity level' in incomplete_fields:
                return "How would you describe your current activity level? Sedentary, lightly active, moderately active, or very active?"
            if 'how often you want to work out' in incomplete_fields:
                return "How many days per week would you like to work out? This helps me create a realistic plan for you."

        # Later stage questions (60%+ complete)
        else:
            if 'how many hours you sleep' in incomplete_fields:
                return "How many hours of sleep do you typically get? Sleep is crucial for fitness and recovery."
            if 'your stress level' in incomplete_fields:
                return "How would you rate your current stress level? Low, moderate, high, or very high?"
            if 'your location' in incomplete_fields:
                return "What city or region are you in? This helps me consider climate and local resources."

        return None

    async def _get_last_bot_question(self, user_id: str) -> Optional[str]:
        """Get the last question the bot asked to provide context for short answers"""
        try:
            # Get last few messages
            recent_history = await MongoDB.get_user_chat_history(user_id, limit=5, days_back=1)
            
            # Look for the last assistant message that contained a question
            for msg in reversed(recent_history):
                if msg['role'] == 'assistant' and ('?' in msg['content'] or any(keyword in msg['content'].lower() for keyword in ['tell me', 'what', 'how', 'could you', 'share', 'rate'])):
                    return msg['content']
            
            return None
        except Exception as e:
            print(f"Error getting last bot question: {e}")
            return None

    async def _extract_user_data_with_ai(self, user_message: str, last_question: str, current_user_data: Dict) -> Dict[str, Any]:
        """🔥 REVOLUTIONARY: Use AI to intelligently extract user data based on context and meaning"""
        try:
            # Create context for AI extraction
            extraction_prompt = f"""You are a data extraction AI that analyzes fitness conversations to extract structured user information.

CONTEXT:
- Last bot question: "{last_question}"
- User's response: "{user_message}"
- Current user data: {json.dumps(current_user_data, default=str)}

EXTRACTION RULES:
1. Extract data based on MEANING and CONTEXT, not just keywords
2. Handle scales, numbers, ratings, and conversational responses
3. Map responses to appropriate database fields
4. Use context to understand what the user is referring to

FIELD MAPPINGS:
- age: integer (13-100)
- weight: float in kg (30-300) 
- height: integer in cm (100-250)
- stress_level: "low", "moderate", "high", "very_high" (also handle 1-10 scales)
- activity_level: "sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"
- fitness_goals: array from ["weight_loss", "muscle_gain", "strength", "endurance", "general_fitness", "flexibility"]
- workout_frequency: integer (0-14) times per week
- sleep_hours: float (3-12)
- gender: "male", "female", "other", "prefer_not_to_say"
- name: string
- location: string

EXAMPLES:
- If asked about stress 1-10 and user says "7" → stress_level: "high" 
- If asked about activity and user says "I go to gym 3 times" → activity_level: "moderately_active", workout_frequency: 3
- If asked about goals and user says "lose some weight" → fitness_goals: ["weight_loss"]
- If asked about height and user says "5'8" → height: 173

OUTPUT FORMAT: Return ONLY a JSON object with extracted fields. If nothing can be extracted, return {{}}.

ANALYZE: {user_message}"""

            response = await openai.ChatCompletion.acreate(
                model="gpt-4.1-nano",
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                # Clean up response to extract JSON
                if '```json' in ai_response:
                    ai_response = ai_response.split('```json')[1].split('```')[0]
                elif '```' in ai_response:
                    ai_response = ai_response.split('```')[1]
                
                extracted_data = json.loads(ai_response)
                
                # Validate extracted data
                validated_data = self._validate_extracted_data(extracted_data)
                
                if validated_data:
                    print(f"🤖 AI extracted: {validated_data}")
                
                return validated_data
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}, Raw response: {ai_response}")
                return {}
                
        except Exception as e:
            print(f"Error in AI extraction: {e}")
            return {}

    def _validate_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean extracted data"""
        validated = {}
        
        # Age validation
        if 'age' in data:
            try:
                age = int(data['age'])
                if 13 <= age <= 100:
                    validated['age'] = age
            except (ValueError, TypeError):
                pass
        
        # Weight validation
        if 'weight' in data:
            try:
                weight = float(data['weight'])
                if 30 <= weight <= 300:
                    validated['weight'] = round(weight, 1)
            except (ValueError, TypeError):
                pass
        
        # Height validation
        if 'height' in data:
            try:
                height = int(data['height'])
                if 100 <= height <= 250:
                    validated['height'] = height
            except (ValueError, TypeError):
                pass
        
        # Stress level validation
        if 'stress_level' in data:
            valid_stress = ['low', 'moderate', 'high', 'very_high']
            if data['stress_level'] in valid_stress:
                validated['stress_level'] = data['stress_level']
        
        # Activity level validation
        if 'activity_level' in data:
            valid_activity = ['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extremely_active']
            if data['activity_level'] in valid_activity:
                validated['activity_level'] = data['activity_level']
        
        # Fitness goals validation
        if 'fitness_goals' in data:
            valid_goals = ['weight_loss', 'muscle_gain', 'strength', 'endurance', 'general_fitness', 'flexibility']
            if isinstance(data['fitness_goals'], list):
                validated_goals = [goal for goal in data['fitness_goals'] if goal in valid_goals]
                if validated_goals:
                    validated['fitness_goals'] = validated_goals
        
        # Workout frequency validation
        if 'workout_frequency' in data:
            try:
                freq = int(data['workout_frequency'])
                if 0 <= freq <= 14:
                    validated['workout_frequency'] = freq
            except (ValueError, TypeError):
                pass
        
        # Sleep hours validation
        if 'sleep_hours' in data:
            try:
                hours = float(data['sleep_hours'])
                if 3 <= hours <= 12:
                    validated['sleep_hours'] = hours
            except (ValueError, TypeError):
                pass
        
        # Gender validation
        if 'gender' in data:
            valid_genders = ['male', 'female', 'other', 'prefer_not_to_say']
            if data['gender'] in valid_genders:
                validated['gender'] = data['gender']
        
        # Name validation
        if 'name' in data:
            if isinstance(data['name'], str) and 1 < len(data['name']) < 50:
                validated['name'] = data['name'].strip().title()
        
        # Location validation
        if 'location' in data:
            if isinstance(data['location'], str) and len(data['location']) > 2:
                validated['location'] = data['location'].strip().title()
        
        return validated

    async def _extract_user_data(self, user_message: str, current_user_data: Dict, user_id: str) -> Dict[str, Any]:
        """🔥 ENHANCED: Smart AI-powered data extraction"""
        extracted_data = {}
        
        # Get context from last bot question
        last_question = await self._get_last_bot_question(user_id)
        
        if last_question:
            # 🔥 NEW: Use AI for intelligent extraction
            ai_extracted = await self._extract_user_data_with_ai(user_message, last_question, current_user_data)
            extracted_data.update(ai_extracted)
        
        # Fallback to basic pattern matching for explicit statements
        basic_extracted = self._extract_explicit_data(user_message.lower(), current_user_data)
        
        # Merge data (AI extraction takes priority)
        for key, value in basic_extracted.items():
            if key not in extracted_data:
                extracted_data[key] = value
        
        return extracted_data

    def _extract_explicit_data(self, message_lower: str, current_user_data: Dict) -> Dict[str, Any]:
        """Basic pattern matching for explicit statements"""
        extracted_data = {}

        # Name extraction
        name_patterns = [
            r"(?:my name is|i'm|i am|call me)\s+([A-Za-z\s]+)",
            r"name\s*:?\s*([A-Za-z\s]+)"
        ]
        for pattern in name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1).strip().title()
                if 1 < len(name) < 50:
                    extracted_data['name'] = name
                break

        # Age extraction (explicit)
        age_patterns = [
            r"\b(\d{1,2})\s*(?:years?\s*old|y/?o)\b",
            r"\bi'?m\s*(\d{1,2})\b",
            r"\bage\s*:?\s*(\d{1,2})\b"
        ]
        for pattern in age_patterns:
            match = re.search(pattern, message_lower)
            if match:
                age = int(match.group(1))
                if 13 <= age <= 100:
                    extracted_data['age'] = age
                break

        # Weight extraction (explicit with units)
        weight_patterns = [
            r"(\d+\.?\d*)\s*(?:kg|kilograms?)\b",
            r"(\d+\.?\d*)\s*(?:lbs?|pounds?)\b",
            r"weigh\s*(\d+\.?\d*)"
        ]
        for pattern in weight_patterns:
            match = re.search(pattern, message_lower)
            if match:
                weight = float(match.group(1))
                if "lb" in pattern or "pound" in pattern:
                    weight *= 0.453592
                if 30 <= weight <= 300:
                    extracted_data['weight'] = round(weight, 1)
                break

        # Height extraction (explicit with units)
        height_patterns = [
            r"(\d+)\s*(?:cm|centimeters?)\b",
            r"(\d+\.?\d*)\s*(?:m|meters?)\b",
            r"(\d+)\s*feet?\s*(\d+)\s*inch",
            r"(\d+)'(\d+)"
        ]
        for pattern in height_patterns:
            match = re.search(pattern, message_lower)
            if match:
                if "feet" in pattern or "'" in pattern:
                    feet = int(match.group(1))
                    inches = int(match.group(2)) if match.group(2) else 0
                    height_cm = (feet * 12 + inches) * 2.54
                elif "m" in pattern and "cm" not in pattern:
                    height_cm = float(match.group(1)) * 100
                else:
                    height_cm = float(match.group(1))
                
                if 100 <= height_cm <= 250:
                    extracted_data['height'] = round(height_cm)
                break

        return extracted_data

    async def _update_user_profile(self, user_id: str, extracted_data: Dict[str, Any]):
        """Update user profile with extracted data"""
        if extracted_data:
            success = await MongoDB.update_user_profile(user_id, extracted_data)
            if success:
                print(f"Updated user profile: {extracted_data}")
                return True
        return False

    async def _should_collect_data(self, user_id: str) -> bool:
        """Determine if we should focus on data collection"""
        user = await MongoDB.get_user(user_id)
        if not user:
            return True
        
        completion = user.get('profile_completion', 0)
        return completion < 70  # Collect data until 70% complete

    async def _create_daily_summary(self, user_id: str):
        """Create daily summary at end of day"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check if summary already exists for today
        existing_summary = await MongoDB.get_daily_summary(user_id, today)
        if existing_summary:
            return  # Already created today's summary

        # Get today's conversations
        today_messages = await MongoDB.get_today_chat_history(user_id)
        if not today_messages:
            return  # No conversations today

        # Get user context for personalization
        user_context = await self._build_user_context(user_id)
        
        # Prepare conversation text for AI summarization
        conversation_text = ""
        for msg in today_messages:
            role = "User" if msg['role'] == 'user' else "FitsBi"
            conversation_text += f"{role}: {msg['content']}\n"

        # Generate summary using AI
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4.1-nano",
                messages=[
                    {
                        "role": "system",
                        "content": """You are creating a daily summary for a user's health and fitness journey. 

Create a concise but comprehensive summary that includes:
1. Key activities, exercises, or health topics discussed
2. Any progress, achievements, or challenges mentioned
3. Goals set or progress toward existing goals
4. Mood, energy levels, or wellbeing indicators
5. Any important health data shared (weight, sleep, etc.)
6. Plans or commitments made for future

Keep it personal and encourage continuity for tomorrow's conversation.
Write in 2nd person (you did, you mentioned, etc.)."""
                    },
                    {
                        "role": "user",
                        "content": f"User Context:\n{user_context}\n\nToday's Conversation:\n{conversation_text}\n\nCreate a daily summary:"
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )

            summary_text = response.choices[0].message.content

            # Extract key information
            key_activities = []
            mood_trends = None
            health_insights = None
            
            # Simple keyword extraction for activities
            activity_keywords = ['workout', 'exercise', 'walk', 'run', 'gym', 'yoga', 'diet', 'meal', 'sleep']
            for keyword in activity_keywords:
                if keyword in conversation_text.lower():
                    key_activities.append(keyword)

            # Save summary
            summary_data = {
                "date": today,
                "summary_text": summary_text,
                "key_activities": key_activities,
                "mood_trends": mood_trends,
                "health_insights": health_insights,
                "conversation_count": len(today_messages),
                "data_updates": {}  # Track any profile updates made today
            }

            await MongoDB.save_daily_summary(user_id, summary_data)
            print(f"Created daily summary for user {user_id}")

        except Exception as e:
            print(f"Error creating daily summary: {e}")

    async def _update_user_summary(self, user_id: str):
        """Update overall user summary weekly"""
        user_summary = await MongoDB.get_user_summary(user_id)
        last_update = user_summary.get('last_updated') if user_summary else None
        
        # Update weekly or if no summary exists
        should_update = (
            not last_update or 
            (datetime.utcnow() - last_update).days >= 7
        )
        
        if not should_update:
            return

        # Get recent daily summaries and user context
        recent_summaries = await MongoDB.get_recent_daily_summaries(user_id, days=14)
        user_context = await self._build_user_context(user_id)
        
        # Prepare data for AI summarization
        summaries_text = ""
        for summary in recent_summaries:
            date_str = summary['date'].strftime('%Y-%m-%d')
            summaries_text += f"{date_str}: {summary['summary_text']}\n"

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4.1-nano",
                messages=[
                    {
                        "role": "system",
                        "content": """You are updating a comprehensive user summary for a health and fitness AI assistant.

Create an updated summary that includes:
1. Overall journey and progress
2. Recent patterns and trends (last 2 weeks)
3. Current health status and fitness level
4. Goals progress and achievements
5. Challenges and areas for improvement
6. Current recommendations and focus areas

This summary helps maintain continuity across conversations. Write in 3rd person."""
                    },
                    {
                        "role": "user",
                        "content": f"User Profile:\n{user_context}\n\nRecent Daily Summaries:\n{summaries_text}\n\nCreate updated user summary:"
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )

            summary_content = response.choices[0].message.content

            # Structure the summary
            summary_parts = summary_content.split('\n\n')
            overall_summary = summary_parts[0] if summary_parts else summary_content
            recent_patterns = summary_parts[1] if len(summary_parts) > 1 else ""
            goals_progress = summary_parts[2] if len(summary_parts) > 2 else ""

            summary_data = {
                "overall_summary": overall_summary,
                "recent_patterns": recent_patterns,
                "health_trends": "",
                "goals_progress": goals_progress,
                "recommendations": ""
            }

            await MongoDB.save_user_summary(user_id, summary_data)
            print(f"Updated user summary for user {user_id}")

        except Exception as e:
            print(f"Error updating user summary: {e}")

    async def generate_response(self, user_id: str, user_message: str) -> str:
        """Generate AI response with data collection and memory management"""
        
        # Get current user data
        user = await MongoDB.get_user(user_id)
        current_user_data = user if user else {}
        
        # 🔥 REVOLUTIONARY: AI-powered data extraction
        extracted_data = await self._extract_user_data(user_message, current_user_data, user_id)
        
        # Update profile if new data found
        if extracted_data:
            await self._update_user_profile(user_id, extracted_data)
        
        # Build comprehensive context
        context = await self._build_user_context(user_id)
        
        # Check if we should focus on data collection
        should_collect = await self._should_collect_data(user_id)
        missing_data_question = None
        if should_collect:
            missing_data_question = await self._identify_missing_data(user_id)
        
        # Prepare AI messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"User Context:\n{context}"}
        ]
        
        # Add data collection guidance if needed
        if missing_data_question and len(user_message.split()) < 10:
            messages.append({
                "role": "system", 
                "content": f"After responding to the user's message, naturally ask this important question: {missing_data_question}"
            })
        
        # 🔥 THE MEMORY FIX: Get and include recent chat history
        try:
            # Get recent conversation history (last 12 messages to avoid token limits)
            recent_history = await MongoDB.get_user_chat_history(user_id, limit=12, days_back=7)
            
            # Add chat history to messages
            for msg in recent_history:
                if msg['role'] in ['user', 'assistant']:
                    # Ensure proper role mapping for OpenAI
                    role = 'assistant' if msg['role'] == 'assistant' else 'user'
                    messages.append({
                        "role": role,
                        "content": msg['content']
                    })
                    
        except Exception as e:
            print(f"Error loading chat history: {e}")
            # Continue without history if there's an error
        
        # Add the current user message last
        messages.append({"role": "user", "content": user_message})

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4.1-nano",
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            
            assistant_message = response.choices[0].message.content
            
            # Save conversation
            await MongoDB.save_chat_message(user_id, {
                "role": "user",
                "content": user_message,
                "extracted_data": extracted_data
            })
            
            await MongoDB.save_chat_message(user_id, {
                "role": "assistant",
                "content": assistant_message
            })
            
            # Trigger daily summary creation (runs async, doesn't block response)
            try:
                await self._create_daily_summary(user_id)
                await self._update_user_summary(user_id)
            except Exception as e:
                print(f"Background task error: {e}")
            
            return assistant_message
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return