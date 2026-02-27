from flask import Blueprint, request, jsonify
from app.models.candidate import Candidate
from app import db
import jwt
from datetime import datetime, timedelta
import os

import random
import string

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def generate_candidate_id():
    """Generate a random 6-digit candidate ID with prefix"""
    suffix = ''.join(random.choices(string.digits, k=6))
    return f"CAND-{suffix}"

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    # Validation
    required_fields = ['name', 'email', 'password', 'position_applied', 'department']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
            
    if Candidate.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
        
    # Generate unique ID
    candidate_id = generate_candidate_id()
    while Candidate.query.filter_by(candidate_id=candidate_id).first():
        candidate_id = generate_candidate_id()
        
    # Create Candidate
    candidate = Candidate(
        candidate_id=candidate_id,
        name=data['name'],
        email=data['email'],
        phone=data.get('phone') or None,
        dob=data.get('dob'),
        current_role=data.get('current_role'),
        total_experience=data.get('total_experience'),
        position_applied=data['position_applied'],
        department=data['department'],
        status='PENDING'
    )
    
    candidate.set_password(data['password'])
    
    db.session.add(candidate)
    db.session.commit()
    
    # Auto Login (Generate Token)
    token_payload = {
        'candidate_id': candidate.candidate_id,
        'email': candidate.email,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    
    token = jwt.encode(token_payload, os.getenv('SECRET_KEY', 'dev-secret-key'), algorithm='HS256')
    
    return jsonify({
        'message': 'Signup successful',
        'token': token,
        'user': candidate.to_dict()
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
        
    candidate = Candidate.query.filter_by(email=email).first()
    
    if not candidate or not candidate.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
        
    # Generate Token
    token_payload = {
        'candidate_id': candidate.candidate_id,
        'email': candidate.email,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    
    token = jwt.encode(token_payload, os.getenv('SECRET_KEY', 'dev-secret-key'), algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': candidate.to_dict()
    })
