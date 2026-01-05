from flask import Blueprint, request, jsonify
from app.models.candidate import Candidate, InterviewAnalysis, TranscriptSegment
from app import db
from datetime import datetime

bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@bp.route('/', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([c.to_dict() for c in candidates])

@bp.route('/', methods=['POST'])
def create_candidate():
    data = request.json
    
    if Candidate.query.filter_by(candidate_id=data['candidate_id']).first():
        return jsonify({'error': 'Candidate ID already exists'}), 400
        
    candidate = Candidate(
        candidate_id=data['candidate_id'],
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        position_applied=data.get('position_applied'),
        department=data.get('department'),
        status='PENDING'
    )
    
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify(candidate.to_dict()), 201

@bp.route('/<id>', methods=['GET'])
def get_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    return jsonify(candidate.to_dict())

@bp.route('/<id>', methods=['PUT'])
def update_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    data = request.json
    
    if 'name' in data: candidate.name = data['name']
    if 'email' in data: candidate.email = data['email']
    if 'phone' in data: candidate.phone = data['phone']
    if 'position_applied' in data: candidate.position_applied = data['position_applied']
    if 'department' in data: candidate.department = data['department']
    if 'status' in data: candidate.status = data['status']
    
    db.session.commit()
    return jsonify(candidate.to_dict())

@bp.route('/<id>', methods=['DELETE'])
def delete_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    db.session.delete(candidate)
    db.session.commit()
    return jsonify({'message': 'Candidate deleted'})
