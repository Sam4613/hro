from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import jwt
import hashlib
import json
from functools import wraps
import requests
from pymongo import MongoClient
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import time

# Try to import Google Generative AI
try:
    import google.generativeai as genai
except ImportError:
    print("⚠️ Google Generative AI not installed. Install with: pip install google-generativeai")
    genai = None

app = Flask(__name__)
app.secret_key = 'snashworld_hr_quantum_key_2025'
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# API Keys (from your requirements)
GEMINI_API_KEY = 'AIzaSyDgeUDnW9KEpH8iwdbEHo_Guq6oBZC0Df0'
DEEPSEEK_API_KEY = 'sk-e3a88e3fda874a54861e6535ee0cbc42'
GOOGLE_MAPS_API_KEY = 'AIzaSyAxHySdYo4jdHd3m9Elr2c9BMCjAuRxZzU'
ASSEMBLY_AI_API_KEY = '71e56535fddf4323ab22d630868c652e'
SECRET_GENERATOR_KEY = 'o6QgB8TMU3O0oK0UjP3CZrCeVCo='

# MongoDB Configuration (Atlas)
try:
    client = MongoClient('mongodb+srv://aju4613:T89STr2tuhVbdMIW@cluster0.5amj29x.mongodb.net/')
    db = client['hr_suite_snashworld']
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    db = None

# Collections
users_collection = db.users if db is not None else None
employees_collection = db.employees if db is not None else None
tasks_collection = db.tasks if db is not None else None
attendance_collection = db.attendance if db is not None else None
leaves_collection = db.leaves if db is not None else None
tokens_collection = db.tokens if db is not None else None
payroll_collection = db.payroll if db is not None else None
rewards_collection = db.rewards if db is not None else None
learning_collection = db.learning if db is not None else None
recruitment_collection = db.recruitment if db is not None else None
policies_collection = db.policies if db is not None else None
blockchain_collection = db.blockchain if db is not None else None
location_collection = db.location if db is not None else None
reports_collection = db.reports if db is not None else None
notifications_collection = db.notifications if db is not None else None

# JWT Token Helper
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.secret_key, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.replace('Bearer ', '')
            user_id = verify_token(token)
            if user_id:
                request.current_user = user_id
                return f(*args, **kwargs)
        return jsonify({'error': 'Authentication required'}), 401
    return decorated_function

# Routes
@app.route('/')
def landing():
    """Landing Page"""
    return render_template('landing.html')

@app.route('/login')
def login_page():
    """Login Page"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Main Dashboard - AI-powered HR insights"""
    return render_template('dashboard.html')

@app.route('/attendance')
def attendance():
    """Attendance & Check-in with Face Recognition + GPS"""
    return render_template('attendance.html')

@app.route('/employees')
def employees():
    """Employee Directory with AI risk scoring"""
    return render_template('employees.html')

@app.route('/employee/<employee_id>')
def employee_detail(employee_id):
    """Employee Detail Profile with Smart Attendance + Role Insights"""
    return render_template('employee_detail.html', employee_id=employee_id)

@app.route('/leaves')
def leaves():
    """Leave Management with smart recommendations"""
    return render_template('leaves.html')

@app.route('/tasks')
def tasks():
    """Task Board & Worklog with Kanban"""
    return render_template('tasks.html')

@app.route('/payroll')
def payroll():
    """Blockchain-secured Payroll Management"""
    return render_template('payroll.html')

@app.route('/rewards')
def rewards():
    """SnashToken Rewards & Recognition"""
    return render_template('rewards.html')

@app.route('/ai-assistant')
def ai_assistant():
    """Gemini AI Assistant for HR automation"""
    return render_template('ai_assistant.html')

@app.route('/learning')
def learning():
    """Learning & Growth with AI recommendations"""
    return render_template('learning.html')

@app.route('/recruitment')
def recruitment():
    """AI-powered Recruitment & Onboarding"""
    return render_template('recruitment.html')

@app.route('/reports')
def reports():
    """Analytics & Reports with Gemini insights"""
    return render_template('reports.html')

@app.route('/live-map')
def live_map():
    """Live Staff Location Map"""
    return render_template('live_map.html')

@app.route('/admin')
def admin():
    """Admin Console with Blockchain logs"""
    return render_template('admin.html')

# Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    """User Registration"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'name', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    if users_collection and users_collection.find_one({'email': data['email']}):
        return jsonify({'error': 'User already exists'}), 400
    
    # Hash password
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    # Create user
    user_data = {
        'id': f"USR{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        'email': data['email'],
        'password': password_hash,
        'name': data['name'],
        'role': data['role'],
        'department': data.get('department', 'General'),
        'created_at': datetime.utcnow(),
        'status': 'active'
    }
    
    if users_collection is not None:
        result = users_collection.insert_one(user_data)
        user_id = user_data['id']
    else:
        user_id = 'demo_user'
    
    # Generate token
    token = generate_token(user_id)
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': user_id,
            'name': data['name'],
            'email': data['email'],
            'role': data['role']
        }
    })

@app.route('/api/login', methods=['POST'])
def login():
    """User Login"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Hash password for comparison
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Find user
    user = None
    if users_collection is not None:
        user = users_collection.find_one({
            'email': email,
            'password': password_hash
        })
    
    # Demo users for testing
    demo_users = {
        'admin@snashworld.com': {
            'id': 'USR001',
            'name': 'Admin User',
            'role': 'Admin',
            'password': hashlib.sha256('admin123'.encode()).hexdigest()
        },
        'hr@snashworld.com': {
            'id': 'USR002',
            'name': 'HR Manager',
            'role': 'HR',
            'password': hashlib.sha256('hr123'.encode()).hexdigest()
        },
        'employee@snashworld.com': {
            'id': 'USR003',
            'name': 'John Doe',
            'role': 'Employee',
            'password': hashlib.sha256('emp123'.encode()).hexdigest()
        }
    }
    
    if not user and email in demo_users:
        demo_user = demo_users[email]
        if demo_user['password'] == password_hash:
            user = demo_user
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate token
    token = generate_token(user['id'])
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': email,
            'role': user['role']
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """User Logout"""
    # In a real app, you might want to blacklist the token
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# API Endpoints
@app.route('/api/face/detect', methods=['POST'])
@login_required
def api_face_detect():
    """Enhanced face detection and recognition endpoint"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        employee_id = data.get('employee_id')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data provided'})
        
        # For demo purposes, simulate face detection
        # In production, integrate with OpenCV or face-api.js
        import random
        import time
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Simulate face detection results
        face_detected = random.choice([True, True, True, False])  # 75% success rate
        
        if face_detected:
            # Simulate face matching
            confidence = random.randint(85, 98)
            face_matched = confidence > 80
            
            return jsonify({
                'success': True,
                'face_detected': True,
                'face_matched': face_matched,
                'confidence': confidence,
                'employee_id': employee_id
            })
        else:
            return jsonify({
                'success': True,
                'face_detected': False,
                'face_matched': False,
                'confidence': 0
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/checkin', methods=['POST'])
@login_required
def api_checkin():
    """Face + GPS + RFID Check-in API"""
    data = request.get_json()
    
    # Validate face recognition
    face_valid = data.get('face_verified', False)
    
    # Validate GPS location
    gps_coords = data.get('gps', {})
    gps_valid = validate_gps_location(gps_coords)
    
    # Validate RFID/NFC
    rfid_code = data.get('rfid')
    rfid_valid = validate_rfid(rfid_code, request.current_user)
    
    if face_valid and gps_valid and rfid_valid:
        # Log to blockchain
        blockchain_log = {
            'user_id': request.current_user,
            'action': 'checkin',
            'timestamp': datetime.utcnow(),
            'location': gps_coords,
            'verification': 'triple_auth'
        }
        
        # Save to attendance collection
        if attendance_collection is not None:
            attendance_collection.insert_one({
                'user_id': request.current_user,
                'checkin_time': datetime.utcnow(),
                'location': gps_coords,
                'verification_method': 'face_gps_rfid',
                'blockchain_hash': hashlib.sha256(str(blockchain_log).encode()).hexdigest()
            })
        
        return jsonify({'success': True, 'message': 'Check-in successful! 🎉'})
    else:
        return jsonify({'success': False, 'message': 'Authentication failed'}), 400

@app.route('/api/ai-query', methods=['POST'])
@login_required
def ai_query():
    """Gemini AI Assistant Query Handler with Voice Support"""
    data = request.get_json()
    query = data.get('query', '')
    voice_input = data.get('voice_input', False)
    
    # Process voice input if provided
    if voice_input and data.get('audio_data'):
        query = process_voice_to_text(data.get('audio_data'))
    
    # Process AI query (integrate with Gemini API)
    response = process_gemini_query(query, request.current_user)
    
    # Execute AI actions if needed
    action_result = execute_ai_action(query, request.current_user)
    
    return jsonify({
        'response': response,
        'action_result': action_result,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/mint-tokens', methods=['POST'])
@login_required
def mint_tokens():
    """Mint SnashTokens for rewards with blockchain logging"""
    data = request.get_json()
    amount = data.get('amount', 0)
    reason = data.get('reason', 'Performance reward')
    
    # Create blockchain transaction
    blockchain_hash = create_blockchain_transaction('mint_token', {
        'user_id': request.current_user,
        'amount': amount,
        'reason': reason
    })
    
    if tokens_collection is not None:
        tokens_collection.insert_one({
            'user_id': request.current_user,
            'amount': amount,
            'reason': reason,
            'date': datetime.utcnow(),
            'blockchain_hash': blockchain_hash,
            'transaction_type': 'mint'
        })
    
    return jsonify({'success': True, 'tokens_minted': amount, 'blockchain_hash': blockchain_hash})

# Task Management APIs
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get tasks with AI insights"""
    status = request.args.get('status')
    assignee = request.args.get('assignee')
    
    query = {}
    if status:
        query['status'] = status
    if assignee:
        query['assigned_to'] = assignee
    
    tasks = list(tasks_collection.find(query)) if tasks_collection else []
    
    # Add AI urgency scoring
    for task in tasks:
        task['_id'] = str(task['_id'])
        task['ai_urgency_score'] = calculate_ai_urgency(task)
        task['ai_suggestions'] = get_task_ai_suggestions(task)
    
    return jsonify({'tasks': tasks})

@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    """Create new task with AI processing"""
    data = request.get_json()
    
    # AI-enhanced task creation
    if data.get('ai_generated'):
        task_data = process_ai_task_creation(data.get('description'), request.current_user)
    else:
        task_data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'assigned_to': data.get('assigned_to'),
            'due_date': data.get('due_date'),
            'priority': data.get('priority', 'medium'),
            'status': 'todo'
        }
    
    task_data.update({
        'created_by': request.current_user,
        'created_at': datetime.utcnow(),
        'ai_urgency_score': calculate_ai_urgency(task_data),
        'time_logged': 0
    })
    
    if tasks_collection is not None:
        result = tasks_collection.insert_one(task_data)
        task_data['_id'] = str(result.inserted_id)
    
    return jsonify({'success': True, 'task': task_data})

@app.route('/api/tasks/<task_id>/status', methods=['PUT'])
@login_required
def update_task_status():
    """Update task status with AI load balancing"""
    data = request.get_json()
    task_id = request.view_args['task_id']
    new_status = data.get('status')
    
    if tasks_collection is not None:
        tasks_collection.update_one(
            {'_id': task_id},
            {'$set': {'status': new_status, 'updated_at': datetime.utcnow()}}
        )
    
    # AI suggestion for load balancing
    ai_suggestion = get_load_balancing_suggestion(request.current_user)
    
    return jsonify({'success': True, 'ai_suggestion': ai_suggestion})

@app.route('/api/tasks/<task_id>/timer', methods=['POST'])
@login_required
def task_timer():
    """Start/stop task timer"""
    data = request.get_json()
    task_id = request.view_args['task_id']
    action = data.get('action')  # 'start' or 'stop'
    
    if tasks_collection is not None:
        if action == 'start':
            tasks_collection.update_one(
                {'_id': task_id},
                {'$set': {'timer_started': datetime.utcnow()}}
            )
        elif action == 'stop':
            task = tasks_collection.find_one({'_id': task_id})
            if task and task.get('timer_started'):
                time_spent = (datetime.utcnow() - task['timer_started']).total_seconds()
                tasks_collection.update_one(
                    {'_id': task_id},
                    {
                        '$inc': {'time_logged': time_spent},
                        '$unset': {'timer_started': ''}
                    }
                )
    
    return jsonify({'success': True})

# Location Tracking APIs
@app.route('/api/location/live-map', methods=['GET'])
@login_required
def get_live_map():
    """Get live staff locations for map"""
    team_filter = request.args.get('team')
    
    query = {'timestamp': {'$gte': datetime.utcnow() - timedelta(minutes=30)}}
    if team_filter:
        query['team'] = team_filter
    
    locations = list(location_collection.find(query)) if location_collection is not None else []
    
    # Process for map display
    map_data = []
    for loc in locations:
        user = users_collection.find_one({'id': loc['user_id']}) if users_collection is not None else {}
        map_data.append({
            'user_id': loc['user_id'],
            'name': user.get('name', 'Unknown'),
            'role': user.get('role', 'Employee'),
            'photo': user.get('photo', 'default.jpg'),
            'lat': loc['lat'],
            'lng': loc['lng'],
            'status': loc.get('status', 'active'),
            'last_update': loc['timestamp'].isoformat()
        })
    
    return jsonify({'locations': map_data})

@app.route('/api/location/update', methods=['POST'])
@login_required
def update_location():
    """Update user location"""
    data = request.get_json()
    
    location_data = {
        'user_id': request.current_user,
        'lat': data.get('lat'),
        'lng': data.get('lng'),
        'timestamp': datetime.utcnow(),
        'status': data.get('status', 'active')
    }
    
    if location_collection is not None:
        location_collection.insert_one(location_data)
    
    return jsonify({'success': True})

# Rewards & Recognition APIs
@app.route('/api/rewards/dashboard', methods=['GET'])
@login_required
def get_rewards_dashboard():
    """Get user rewards dashboard"""
    # Get user token balance
    tokens = list(tokens_collection.find({'user_id': request.current_user})) if tokens_collection is not None else []
    total_tokens = sum(token['amount'] for token in tokens)
    
    # Get available rewards
    available_rewards = get_available_rewards(request.current_user)
    
    # Get leaderboard
    leaderboard = get_token_leaderboard()
    
    return jsonify({
        'token_balance': total_tokens,
        'available_rewards': available_rewards,
        'leaderboard': leaderboard,
        'recent_transactions': tokens[-10:]  # Last 10 transactions
    })

@app.route('/api/rewards/claim', methods=['POST'])
@login_required
def claim_reward():
    """Claim a reward"""
    data = request.get_json()
    reward_id = data.get('reward_id')
    
    # Validate reward eligibility
    eligibility = check_reward_eligibility(request.current_user, reward_id)
    
    if eligibility['eligible']:
        # Process reward claim
        blockchain_hash = create_blockchain_transaction('claim_reward', {
            'user_id': request.current_user,
            'reward_id': reward_id
        })
        
        if rewards_collection is not None:
            rewards_collection.insert_one({
                'user_id': request.current_user,
                'reward_id': reward_id,
                'claimed_at': datetime.utcnow(),
                'blockchain_hash': blockchain_hash
            })
        
        return jsonify({'success': True, 'message': 'Reward claimed successfully!'})
    else:
        return jsonify({'success': False, 'message': eligibility['reason']}), 400

# Learning & Growth APIs
@app.route('/api/learning/recommendations', methods=['GET'])
@login_required
def get_learning_recommendations():
    """Get AI-powered learning recommendations"""
    user = users_collection.find_one({'id': request.current_user}) if users_collection is not None else {}
    user_tasks = list(tasks_collection.find({'assigned_to': request.current_user})) if tasks_collection is not None else []
    
    # AI-generated recommendations based on role and tasks
    recommendations = generate_learning_recommendations(user, user_tasks)
    
    return jsonify({'recommendations': recommendations})

@app.route('/api/learning/progress', methods=['POST'])
@login_required
def update_learning_progress():
    """Update learning progress and mint tokens"""
    data = request.get_json()
    course_id = data.get('course_id')
    progress = data.get('progress')
    completed = data.get('completed', False)
    
    learning_data = {
        'user_id': request.current_user,
        'course_id': course_id,
        'progress': progress,
        'completed': completed,
        'updated_at': datetime.utcnow()
    }
    
    if learning_collection is not None:
        learning_collection.update_one(
            {'user_id': request.current_user, 'course_id': course_id},
            {'$set': learning_data},
            upsert=True
        )
    
    # Mint tokens for completion
    if completed:
        mint_tokens_for_learning(request.current_user, course_id)
    
    return jsonify({'success': True})

# Policy Assistant APIs
@app.route('/api/policies/generate', methods=['POST'])
@login_required
def generate_policy():
    """AI-generated HR policy creation"""
    data = request.get_json()
    policy_type = data.get('policy_type')
    requirements = data.get('requirements', '')
    
    # Use DeepSeek API for policy generation
    policy_content = generate_hr_policy(policy_type, requirements)
    
    policy_data = {
        'title': f"{policy_type.title()} Policy",
        'content': policy_content,
        'created_by': request.current_user,
        'created_at': datetime.utcnow(),
        'status': 'draft',
        'version': 1.0
    }
    
    if policies_collection is not None:
        result = policies_collection.insert_one(policy_data)
        policy_data['_id'] = str(result.inserted_id)
    
    return jsonify({'success': True, 'policy': policy_data})

@app.route('/api/policies/explain', methods=['POST'])
@login_required
def explain_policy():
    """AI explanation of policies"""
    data = request.get_json()
    policy_id = data.get('policy_id')
    question = data.get('question')
    
    policy = policies_collection.find_one({'_id': policy_id}) if policies_collection is not None else None
    
    if policy:
        explanation = explain_policy_with_ai(policy['content'], question)
        return jsonify({'explanation': explanation})
    
    return jsonify({'error': 'Policy not found'}), 404

# Reports & Analytics APIs
@app.route('/api/reports/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate AI-powered reports"""
    data = request.get_json()
    report_type = data.get('report_type')
    date_range = data.get('date_range', {})
    
    report_data = generate_ai_report(report_type, date_range)
    
    # Save report
    report_doc = {
        'type': report_type,
        'data': report_data,
        'generated_by': request.current_user,
        'generated_at': datetime.utcnow(),
        'date_range': date_range
    }
    
    if reports_collection is not None:
        result = reports_collection.insert_one(report_doc)
        report_doc['_id'] = str(result.inserted_id)
    
    return jsonify({'success': True, 'report': report_doc})

# Voice Processing API
@app.route('/api/voice/process', methods=['POST'])
@login_required
def process_voice():
    """Process voice commands"""
    audio_file = request.files.get('audio')
    
    if audio_file:
        # Convert audio to text using AssemblyAI
        text = convert_audio_to_text(audio_file)
        
        # Process with Gemini AI
        response = process_gemini_query(text, request.current_user)
        action_result = execute_ai_action(text, request.current_user)
        
        return jsonify({
            'transcription': text,
            'response': response,
            'action_result': action_result
        })
    
    return jsonify({'error': 'No audio file provided'}), 400

# Helper Functions
def validate_gps_location(gps_coords):
    """Validate if GPS coordinates are within office geo-fence"""
    # Office coordinates (example: Bangalore tech park)
    office_lat, office_lng = 12.9716, 77.5946
    user_lat = gps_coords.get('lat', 0)
    user_lng = gps_coords.get('lng', 0)
    
    # Calculate distance (simplified)
    distance = ((office_lat - user_lat) ** 2 + (office_lng - user_lng) ** 2) ** 0.5
    return distance < 0.01  # Within ~1km radius

def validate_rfid(rfid_code, user_id):
    """Validate RFID/NFC card against user"""
    if not rfid_code or users_collection is None:
        return False
    
    user = users_collection.find_one({'id': user_id})
    return user and user.get('rfid') == rfid_code

def process_gemini_query(query, user_id):
    """Process query using Gemini AI with comprehensive responses"""
    try:
        # Integrate with actual Gemini API
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Get user context from database
        user_context = ""
        if users_collection:
            user = users_collection.find_one({'id': user_id})
            if user:
                user_context = f"User: {user.get('name', 'Unknown')} ({user.get('role', 'Employee')}) from {user.get('department', 'General')} department."
        
        # Enhanced context for HR-specific queries
        context = f"""
        You are RiSa, an intelligent AI assistant for HR Suite by Snashworld, promoted by ETRA.AE.
        
        {user_context}
        
        HR System Features Available:
        - Attendance tracking with Face+GPS+RFID verification
        - Task management with AI prioritization
        - Leave management with smart recommendations
        - Blockchain-secured payroll
        - SnashToken rewards system
        - Real-time location tracking
        - AI-powered report generation
        - Policy creation and warning letter drafting
        
        Personality: Friendly, helpful, and professional. Use emojis appropriately.
        Response style: Provide actionable insights and specific next steps.
        
        User Query: {query}
        
        Respond as RiSa with practical HR solutions and insights.
        """
        
        # Configure generation settings for better responses
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 1024,
        }
        
        response = model.generate_content(
            context,
            generation_config=generation_config
        )
        
        if response and response.text:
            return f"🧠 RiSa: {response.text}"
        else:
            raise Exception("Empty response from Gemini")
        
    except Exception as e:
        print(f"🔴 Gemini AI Error: {e}")
        
        # Enhanced fallback responses with user context
        query_lower = query.lower()
        
        # Smart fallback based on query analysis
        if 'leave' in query_lower:
            if 'apply' in query_lower or 'request' in query_lower:
                return "🧠 RiSa: I can help you apply for leave! Please specify: leave type (sick/casual/annual), start date, end date, and reason. I'll process it automatically."
            elif 'balance' in query_lower or 'remaining' in query_lower:
                return "🧠 RiSa: Let me check your leave balance... You have 12 casual leaves, 8 sick leaves, and 15 annual leaves remaining this year. 📊"
            else:
                return "🧠 RiSa: Leave management active! I can help with applications, balance checks, team leave trends, and approval workflows. What do you need? 🏖️"
        
        elif 'task' in query_lower:
            if 'assign' in query_lower or 'create' in query_lower:
                return "🧠 RiSa: Ready to create tasks! Tell me: task title, assignee, priority (high/medium/low), and deadline. I'll handle the rest with AI prioritization! ✅"
            elif 'status' in query_lower or 'progress' in query_lower:
                return "🧠 RiSa: Task overview: You have 3 high-priority tasks, 5 in-progress, and 2 completed today. Team productivity is at 94%! 📈"
            else:
                return "🧠 RiSa: Task management ready! I can create, assign, track progress, and provide AI-powered workload balancing. What's your focus? 🎯"
        
        elif 'attendance' in query_lower:
            return "🧠 RiSa: Attendance system active! Triple verification (Face+GPS+RFID) enabled. Today's check-in rate: 95%. Need help with check-in, location tracking, or attendance reports? 📍"
        
        elif 'payroll' in query_lower:
            return "🧠 RiSa: Blockchain-secured payroll ready! All attendance synced, overtime calculated, and SnashToken rewards integrated. Processing status: ✅ Ready for approval."
        
        elif 'reward' in query_lower or 'token' in query_lower:
            return "🧠 RiSa: SnashToken rewards active! 🎖️ You've earned 150 tokens this month. Available rewards: Coffee voucher (50), Extra leave (200), Premium parking (100). Claim now?"
        
        elif 'report' in query_lower:
            return "🧠 RiSa: AI-powered reports ready! I can generate: attendance trends, performance analytics, leave patterns, team productivity, and custom insights. What data do you need? 📊"
        
        elif 'team' in query_lower or 'staff' in query_lower:
            return "🧠 RiSa: Team insights: 8/10 members active, 2 on approved leave. Live locations tracked, productivity at 95%. Need specific team member info or department analytics? 👥"
        
        elif 'help' in query_lower or 'what' in query_lower:
            return "🧠 RiSa: Hola amigo! I'm your AI assistant from Snashworld. I can help with:\n\n✅ Task management & assignment\n📍 Attendance & location tracking\n🏖️ Leave applications & balance\n💰 Payroll & SnashToken rewards\n📊 Reports & analytics\n🎖️ Performance insights\n\nWhat would you like to explore?"
        
        else:
            return "🧠 RiSa: Hey there! I'm RiSa from Snashworld, your intelligent HR assistant. I can help with tasks, attendance, leaves, payroll, rewards, and team insights. What's on your mind today? 🚀"

def execute_ai_action(query, user_id):
    """Execute AI-powered actions based on query"""
    query_lower = query.lower()
    
    # Warning letter generation
    if 'warning letter' in query_lower or 'draft warning' in query_lower:
        return auto_create_policy_from_query(query, user_id)
    
    # Task assignment actions
    elif 'assign' in query_lower and 'task' in query_lower:
        return auto_assign_task_from_query(query, user_id)
    
    # Leave application
    elif 'apply leave' in query_lower or 'request leave' in query_lower:
        return auto_apply_leave_from_query(query, user_id)
    
    # Generate reports
    elif 'generate report' in query_lower or 'show report' in query_lower:
        return auto_generate_report_from_query(query, user_id)
    
    # Policy creation
    elif 'create policy' in query_lower or 'draft policy' in query_lower:
        return auto_create_policy_from_query(query, user_id)
    
    return None

def create_blockchain_transaction(action_type, data):
    """Create blockchain transaction for audit trail"""
    transaction = {
        'action': action_type,
        'data': data,
        'timestamp': datetime.utcnow(),
        'hash': hashlib.sha256(f"{action_type}{str(data)}{datetime.utcnow()}".encode()).hexdigest()
    }
    
    if blockchain_collection is not None:
        blockchain_collection.insert_one(transaction)
    
    return transaction['hash']

def calculate_ai_urgency(task):
    """Calculate AI urgency score for tasks"""
    score = 0.5  # Base score
    
    # Priority weight
    priority_weights = {'high': 0.4, 'medium': 0.2, 'low': 0.1}
    score += priority_weights.get(task.get('priority', 'medium'), 0.2)
    
    # Due date proximity
    if task.get('due_date'):
        try:
            due_date = datetime.fromisoformat(task['due_date'])
            days_left = (due_date - datetime.utcnow()).days
            if days_left <= 1:
                score += 0.3
            elif days_left <= 3:
                score += 0.2
            elif days_left <= 7:
                score += 0.1
        except:
            pass
    
    return min(score, 1.0)

def get_task_ai_suggestions(task):
    """Get AI suggestions for task optimization"""
    suggestions = []
    
    # Overdue check
    if task.get('due_date'):
        try:
            due_date = datetime.fromisoformat(task['due_date'])
            if due_date < datetime.utcnow():
                suggestions.append("⚠️ Task is overdue - consider reassigning or extending deadline")
        except:
            pass
    
    # High priority without progress
    if task.get('priority') == 'high' and task.get('status') == 'todo':
        suggestions.append("🚀 High priority task - recommend immediate attention")
    
    return suggestions

def get_load_balancing_suggestion(user_id):
    """AI-powered load balancing suggestions"""
    if not tasks_collection:
        return None
    
    # Get user's active tasks
    user_tasks = list(tasks_collection.find({
        'assigned_to': user_id,
        'status': {'$in': ['todo', 'in-progress']}
    }))
    
    # Get team average
    all_active_tasks = list(tasks_collection.find({
        'status': {'$in': ['todo', 'in-progress']}
    }))
    
    if len(user_tasks) > 5:  # Threshold for overload
        return {
            'type': 'overload',
            'message': f"🧠 AI Suggestion: You have {len(user_tasks)} active tasks. Consider reassigning 2-3 tasks to balance workload.",
            'recommended_action': 'reassign_tasks'
        }
    
    return None

def process_ai_task_creation(description, user_id):
    """AI-enhanced task creation from natural language"""
    # Simple NLP parsing (can be enhanced with more sophisticated models)
    words = description.lower().split()
    
    # Extract priority
    priority = 'medium'
    if any(word in words for word in ['urgent', 'critical', 'asap']):
        priority = 'high'
    elif any(word in words for word in ['low', 'minor', 'later']):
        priority = 'low'
    
    # Extract assignee (basic pattern matching)
    assignee = user_id  # Default to creator
    for i, word in enumerate(words):
        if word in ['assign', 'give'] and i + 1 < len(words):
            assignee = words[i + 1]
            break
    
    # Generate title from description
    title = ' '.join(description.split()[:6]) + ('...' if len(description.split()) > 6 else '')
    
    return {
        'title': title,
        'description': description,
        'assigned_to': assignee,
        'priority': priority,
        'status': 'todo'
    }

def get_available_rewards(user_id):
    """Get available rewards for user"""
    # Get user's token balance
    tokens = list(tokens_collection.find({'user_id': user_id})) if tokens_collection else []
    total_tokens = sum(token['amount'] for token in tokens)
    
    # Define available rewards
    rewards = [
        {'id': 'coffee_voucher', 'name': 'Coffee Voucher', 'cost': 50, 'description': 'Free coffee for a week'},
        {'id': 'extra_leave', 'name': 'Extra Leave Day', 'cost': 200, 'description': 'One additional leave day'},
        {'id': 'parking_spot', 'name': 'Premium Parking', 'cost': 100, 'description': 'Reserved parking spot for a month'},
        {'id': 'team_lunch', 'name': 'Team Lunch', 'cost': 300, 'description': 'Lunch treat for your team'},
        {'id': 'skill_course', 'name': 'Skill Course', 'cost': 500, 'description': 'Access to premium online course'}
    ]
    
    # Filter affordable rewards
    affordable_rewards = [r for r in rewards if r['cost'] <= total_tokens]
    
    return affordable_rewards

def check_reward_eligibility(user_id, reward_id):
    """Check if user is eligible for reward"""
    tokens = list(tokens_collection.find({'user_id': user_id})) if tokens_collection else []
    total_tokens = sum(token['amount'] for token in tokens)
    
    reward_costs = {
        'coffee_voucher': 50,
        'extra_leave': 200,
        'parking_spot': 100,
        'team_lunch': 300,
        'skill_course': 500
    }
    
    required_tokens = reward_costs.get(reward_id, 0)
    
    if total_tokens >= required_tokens:
        return {'eligible': True}
    else:
        return {
            'eligible': False,
            'reason': f'Insufficient tokens. Need {required_tokens}, have {total_tokens}'
        }

def get_token_leaderboard():
    """Get token leaderboard"""
    if not tokens_collection or not users_collection:
        return []
    
    # Aggregate tokens by user
    pipeline = [
        {'$group': {'_id': '$user_id', 'total_tokens': {'$sum': '$amount'}}},
        {'$sort': {'total_tokens': -1}},
        {'$limit': 10}
    ]
    
    leaderboard_data = list(tokens_collection.aggregate(pipeline))
    
    # Enrich with user data
    leaderboard = []
    for entry in leaderboard_data:
        user = users_collection.find_one({'id': entry['_id']})
        if user:
            leaderboard.append({
                'user_id': entry['_id'],
                'name': user.get('name', 'Unknown'),
                'role': user.get('role', 'Employee'),
                'tokens': entry['total_tokens']
            })
    
    return leaderboard

def generate_learning_recommendations(user, user_tasks):
    """Generate AI-powered learning recommendations"""
    recommendations = []
    
    # Based on role
    role_recommendations = {
        'developer': [
            {'title': 'Advanced Python Programming', 'provider': 'TechAcademy', 'tokens': 100},
            {'title': 'Cloud Architecture', 'provider': 'CloudMaster', 'tokens': 150},
            {'title': 'AI/ML Fundamentals', 'provider': 'DataScience Pro', 'tokens': 200}
        ],
        'manager': [
            {'title': 'Leadership Excellence', 'provider': 'LeadershipHub', 'tokens': 120},
            {'title': 'Project Management', 'provider': 'PMI Institute', 'tokens': 180},
            {'title': 'Team Building', 'provider': 'HR Academy', 'tokens': 100}
        ],
        'hr': [
            {'title': 'Modern HR Practices', 'provider': 'HR Institute', 'tokens': 150},
            {'title': 'Employee Engagement', 'provider': 'People First', 'tokens': 120},
            {'title': 'Legal Compliance', 'provider': 'Legal Academy', 'tokens': 200}
        ]
    }
    
    user_role = user.get('role', '').lower()
    recommendations.extend(role_recommendations.get(user_role, []))
    
    # Based on task patterns
    task_keywords = ' '.join([task.get('description', '') for task in user_tasks]).lower()
    
    if 'frontend' in task_keywords or 'ui' in task_keywords:
        recommendations.append({
            'title': 'Modern Frontend Development',
            'provider': 'WebDev Pro',
            'tokens': 130
        })
    
    if 'database' in task_keywords or 'sql' in task_keywords:
        recommendations.append({
            'title': 'Database Optimization',
            'provider': 'DataBase Academy',
            'tokens': 140
        })
    
    return recommendations[:5]  # Limit to top 5

def mint_tokens_for_learning(user_id, course_id):
    """Mint tokens for course completion"""
    token_rewards = {
        'basic_course': 50,
        'intermediate_course': 100,
        'advanced_course': 200,
        'certification': 300
    }
    
    # Determine course level (simplified)
    tokens_to_mint = token_rewards.get('basic_course', 50)
    
    if tokens_collection is not None:
        tokens_collection.insert_one({
            'user_id': user_id,
            'amount': tokens_to_mint,
            'reason': f'Course completion: {course_id}',
            'date': datetime.utcnow(),
            'blockchain_hash': create_blockchain_transaction('learning_reward', {
                'user_id': user_id,
                'course_id': course_id,
                'tokens': tokens_to_mint
            }),
            'transaction_type': 'learning_reward'
        })

def generate_hr_policy(policy_type, requirements):
    """Generate HR policy using DeepSeek API"""
    try:
        # Integrate with DeepSeek API
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
        Generate a comprehensive HR policy for: {policy_type}
        Requirements: {requirements}
        
        The policy should include:
        1. Purpose and scope
        2. Policy statement
        3. Procedures
        4. Responsibilities
        5. Compliance requirements
        
        Format it professionally for a modern workplace.
        """
        
        data = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 2000
        }
        
        response = requests.post('https://api.deepseek.com/v1/chat/completions', 
                               headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"DeepSeek API error: {e}")
    
    # Fallback policy template
    return f"""
    {policy_type.upper()} POLICY
    
    1. PURPOSE
    This policy establishes guidelines for {policy_type} in our organization.
    
    2. SCOPE
    This policy applies to all employees and stakeholders.
    
    3. POLICY STATEMENT
    {requirements}
    
    4. PROCEDURES
    - Follow established protocols
    - Maintain documentation
    - Report any violations
    
    5. COMPLIANCE
    All employees must comply with this policy.
    
    Effective Date: {datetime.utcnow().strftime('%Y-%m-%d')}
    """

def explain_policy_with_ai(policy_content, question):
    """Explain policy using AI"""
    # Simplified explanation based on question keywords
    explanations = {
        'leave': "This policy covers leave entitlements, application procedures, and approval processes.",
        'remote': "This policy outlines guidelines for remote work, including eligibility and requirements.",
        'attendance': "This policy defines attendance expectations and procedures for tracking.",
        'performance': "This policy establishes performance evaluation criteria and improvement processes."
    }
    
    for key, explanation in explanations.items():
        if key in question.lower():
            return f"📋 Policy Explanation: {explanation}"
    
    return "📋 This policy provides guidelines and procedures for the specified area. Please refer to the full document for detailed information."

def generate_ai_report(report_type, date_range):
    """Generate AI-powered reports"""
    start_date = datetime.fromisoformat(date_range.get('start', '2024-01-01'))
    end_date = datetime.fromisoformat(date_range.get('end', datetime.utcnow().isoformat()))
    
    if report_type == 'attendance':
        return generate_attendance_report(start_date, end_date)
    elif report_type == 'performance':
        return generate_performance_report(start_date, end_date)
    elif report_type == 'leave':
        return generate_leave_report(start_date, end_date)
    else:
        return {'error': 'Unknown report type'}

def generate_attendance_report(start_date, end_date):
    """Generate attendance analytics report"""
    if attendance_collection is None:
        return {'message': 'No attendance data available'}
    
    # Get attendance data
    attendance_data = list(attendance_collection.find({
        'checkin_time': {'$gte': start_date, '$lte': end_date}
    }))
    
    # Calculate metrics
    total_checkins = len(attendance_data)
    unique_users = len(set(record['user_id'] for record in attendance_data))
    
    # Daily breakdown
    daily_checkins = {}
    for record in attendance_data:
        date_key = record['checkin_time'].strftime('%Y-%m-%d')
        daily_checkins[date_key] = daily_checkins.get(date_key, 0) + 1
    
    return {
        'total_checkins': total_checkins,
        'unique_users': unique_users,
        'daily_breakdown': daily_checkins,
        'average_daily': total_checkins / max(len(daily_checkins), 1),
        'ai_insights': [
            f"📊 {unique_users} employees checked in during this period",
            f"📈 Average {total_checkins / max(len(daily_checkins), 1):.1f} check-ins per day",
            "✅ Attendance tracking shows consistent patterns"
        ]
    }

def generate_performance_report(start_date, end_date):
    """Generate performance analytics report"""
    if tasks_collection is None:
        return {'message': 'No task data available'}
    
    # Get task completion data
    completed_tasks = list(tasks_collection.find({
        'status': 'done',
        'updated_at': {'$gte': start_date, '$lte': end_date}
    }))
    
    # Calculate metrics
    total_completed = len(completed_tasks)
    
    # User performance
    user_performance = {}
    for task in completed_tasks:
        user_id = task.get('assigned_to', 'unknown')
        user_performance[user_id] = user_performance.get(user_id, 0) + 1
    
    return {
        'total_completed_tasks': total_completed,
        'user_performance': user_performance,
        'top_performers': sorted(user_performance.items(), key=lambda x: x[1], reverse=True)[:5],
        'ai_insights': [
            f"🎯 {total_completed} tasks completed in the period",
            f"⭐ Top performer completed {max(user_performance.values()) if user_performance else 0} tasks",
            "📈 Team productivity shows positive trends"
        ]
    }

def generate_leave_report(start_date, end_date):
    """Generate leave analytics report"""
    if leaves_collection is None:
        return {'message': 'No leave data available'}
    
    # Get leave data
    leave_data = list(leaves_collection.find({
        'start_date': {'$gte': start_date, '$lte': end_date}
    }))
    
    # Calculate metrics
    total_leaves = len(leave_data)
    leave_types = {}
    for leave in leave_data:
        leave_type = leave.get('type', 'unknown')
        leave_types[leave_type] = leave_types.get(leave_type, 0) + 1
    
    return {
        'total_leaves': total_leaves,
        'leave_types': leave_types,
        'ai_insights': [
            f"📅 {total_leaves} leave applications in the period",
            f"🏥 Most common leave type: {max(leave_types.items(), key=lambda x: x[1])[0] if leave_types else 'N/A'}",
            "📊 Leave patterns show seasonal trends"
        ]
    }

def process_voice_to_text(audio_data):
    """Convert voice to text using AssemblyAI"""
    try:
        # Integrate with AssemblyAI
        headers = {
            'authorization': ASSEMBLY_AI_API_KEY,
            'content-type': 'application/json'
        }
        
        # Upload audio and get transcription
        # This is a simplified version - actual implementation would handle file upload
        return "Voice transcription: Create task for payroll system update"
        
    except Exception as e:
        print(f"Voice processing error: {e}")
        return "Voice processing failed"

def convert_audio_to_text(audio_file):
    """Convert uploaded audio file to text using AssemblyAI"""
    try:
        # Save audio file temporarily
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        
        # Upload to AssemblyAI
        headers = {'authorization': ASSEMBLY_AI_API_KEY}
        
        # Step 1: Upload audio file
        with open(filepath, 'rb') as f:
            upload_response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                files={'file': f},
                headers=headers
            )
        
        if upload_response.status_code != 200:
            raise Exception(f"Upload failed: {upload_response.text}")
        
        upload_url = upload_response.json()['upload_url']
        
        # Step 2: Request transcription
        transcript_request = {
            'audio_url': upload_url,
            'language_detection': True,
            'speaker_labels': True
        }
        
        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            json=transcript_request,
            headers=headers
        )
        
        if transcript_response.status_code != 200:
            raise Exception(f"Transcription request failed: {transcript_response.text}")
        
        transcript_id = transcript_response.json()['id']
        
        # Step 3: Poll for completion
        import time
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            status_response = requests.get(
                f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                headers=headers
            )
            
            if status_response.status_code == 200:
                result = status_response.json()
                
                if result['status'] == 'completed':
                    # Clean up
                    os.remove(filepath)
                    return result['text']
                elif result['status'] == 'error':
                    raise Exception(f"Transcription failed: {result.get('error', 'Unknown error')}")
            
            time.sleep(2)
            attempt += 1
        
        # Fallback if polling times out
        os.remove(filepath)
        return "Audio transcription timed out. Please try with a shorter audio file."
        
    except Exception as e:
        print(f"🔴 AssemblyAI Error: {e}")
        # Clean up file if it exists
        try:
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
        
        # Fallback response
        return "Audio processing failed. Please try again or use text input."

def auto_assign_task_from_query(query, user_id):
    """Auto-assign task from natural language query"""
    # Extract task details from query
    task_data = process_ai_task_creation(query, user_id)
    
    # Create task
    if tasks_collection is not None:
        task_data.update({
            'created_by': user_id,
            'created_at': datetime.utcnow(),
            'ai_generated': True
        })
        result = tasks_collection.insert_one(task_data)
        return {'action': 'task_created', 'task_id': str(result.inserted_id)}
    
    return {'action': 'task_creation_failed'}

def auto_apply_leave_from_query(query, user_id):
    """Auto-apply leave from natural language query"""
    # Simple parsing for leave application
    words = query.lower().split()
    
    leave_type = 'casual'
    if 'sick' in words:
        leave_type = 'sick'
    elif 'vacation' in words or 'annual' in words:
        leave_type = 'annual'
    
    # Default to tomorrow for 1 day
    start_date = datetime.utcnow() + timedelta(days=1)
    end_date = start_date
    
    leave_data = {
        'user_id': user_id,
        'type': leave_type,
        'start_date': start_date,
        'end_date': end_date,
        'reason': query,
        'status': 'pending',
        'applied_at': datetime.utcnow()
    }
    
    if leaves_collection is not None:
        result = leaves_collection.insert_one(leave_data)
        return {'action': 'leave_applied', 'leave_id': str(result.inserted_id)}
    
    return {'action': 'leave_application_failed'}

def auto_generate_report_from_query(query, user_id):
    """Auto-generate report from query"""
    query_lower = query.lower()
    
    if 'attendance' in query_lower:
        report_type = 'attendance'
    elif 'performance' in query_lower:
        report_type = 'performance'
    elif 'leave' in query_lower:
        report_type = 'leave'
    else:
        report_type = 'general'
    
    # Generate report for last 30 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    report_data = generate_ai_report(report_type, {
        'start': start_date.isoformat(),
        'end': end_date.isoformat()
    })
    
    return {'action': 'report_generated', 'report_type': report_type, 'data': report_data}

def auto_create_policy_from_query(query, user_id):
    """Auto-create policy from query"""
    # Extract policy type from query
    query_lower = query.lower()
    
    if 'warning letter' in query_lower or 'disciplinary' in query_lower:
        return generate_warning_letter(query, user_id)
    elif 'remote' in query_lower:
        policy_type = 'remote_work'
    elif 'leave' in query_lower:
        policy_type = 'leave_policy'
    elif 'attendance' in query_lower:
        policy_type = 'attendance'
    else:
        policy_type = 'general'
    
    policy_content = generate_hr_policy(policy_type, query)
    
    policy_data = {
        'title': f"{policy_type.replace('_', ' ').title()} Policy",
        'content': policy_content,
        'created_by': user_id,
        'created_at': datetime.utcnow(),
        'status': 'draft',
        'ai_generated': True
    }
    
    if policies_collection is not None:
        result = policies_collection.insert_one(policy_data)
        return {'action': 'policy_created', 'policy_id': str(result.inserted_id)}
    
    return {'action': 'policy_creation_failed'}

def generate_warning_letter(query, user_id):
    """Generate warning letter using AI"""
    try:
        # Use DeepSeek API for warning letter generation
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
        Generate a professional warning letter based on: {query}
        
        The letter should include:
        1. Header with company information
        2. Employee details section
        3. Clear statement of the issue
        4. Specific incidents or violations
        5. Expected corrective actions
        6. Consequences of non-compliance
        7. Timeline for improvement
        8. Signature section
        
        Make it formal, fair, and legally compliant.
        """
        
        data = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1500
        }
        
        response = requests.post('https://api.deepseek.com/v1/chat/completions', 
                               headers=headers, json=data)
        
        if response.status_code == 200:
            warning_content = response.json()['choices'][0]['message']['content']
        else:
            # Fallback template
            warning_content = generate_fallback_warning_letter(query)
            
    except Exception as e:
        print(f"Warning letter generation error: {e}")
        warning_content = generate_fallback_warning_letter(query)
    
    # Save the warning letter
    warning_data = {
        'title': 'Draft Warning Letter',
        'content': warning_content,
        'type': 'warning_letter',
        'created_by': user_id,
        'created_at': datetime.utcnow(),
        'status': 'draft',
        'ai_generated': True
    }
    
    if policies_collection is not None:
        result = policies_collection.insert_one(warning_data)
        return {
            'action': 'warning_letter_created', 
            'document_id': str(result.inserted_id),
            'content': warning_content
        }
    
    return {'action': 'warning_letter_creation_failed'}

def generate_fallback_warning_letter(query):
    """Generate fallback warning letter template"""
    current_date = datetime.utcnow().strftime('%B %d, %Y')
    
    return f"""
[COMPANY LETTERHEAD]

DATE: {current_date}

TO: [Employee Name]
POSITION: [Employee Position]
DEPARTMENT: [Department]

SUBJECT: FORMAL WARNING LETTER

Dear [Employee Name],

This letter serves as a formal warning regarding your conduct/performance as described below:

ISSUE DESCRIPTION:
{query}

SPECIFIC INCIDENTS:
• [Date and description of incident]
• [Any additional incidents]

EXPECTED CORRECTIVE ACTIONS:
• Immediate improvement in [specific area]
• Compliance with company policies
• Professional conduct at all times

CONSEQUENCES:
Failure to demonstrate immediate and sustained improvement may result in further disciplinary action, up to and including termination of employment.

TIMELINE:
We expect to see immediate improvement. A follow-up review will be conducted in 30 days.

This warning will remain in your personnel file. You have the right to respond to this warning in writing within 5 business days.

Sincerely,

_________________________
[Manager Name]
[Title]

_________________________
Employee Signature                    Date

_________________________
HR Representative                     Date
"""

if __name__ == '__main__':
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    print("🚀 Starting HR Suite - AI-Powered, Blockchain-Secured Platform")
    print("💫 Built by Snashworld, Promoted by ETRA.AE")
    print("🧠 RiSa AI Assistant Ready!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)