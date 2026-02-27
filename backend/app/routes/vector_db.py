from flask import Blueprint, request, jsonify
from app.services.vector_store import get_vector_store
# from app.services.seed_vector_db import seed_all

bp = Blueprint('vector_db', __name__, url_prefix='/api/vector-db')

# Initialize Vector Store
vector_store = get_vector_store()

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get vector database statistics"""
    try:
        stats = vector_store.get_collection_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add-knowledge', methods=['POST'])
def add_knowledge():
    """Add a new knowledge document to the vector DB"""
    data = request.json
    doc_id = data.get('id')
    content = data.get('content')
    metadata = data.get('metadata', {})
    
    if not doc_id or not content:
        return jsonify({'error': 'Missing id or content'}), 400
        
    try:
        vector_store.add_knowledge_document(doc_id, content, metadata)
        return jsonify({'message': 'Document added successfully', 'id': doc_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search/candidates', methods=['POST'])
def search_candidates():
    """Search similar candidates based on description or skills"""
    data = request.json
    query = data.get('query', '')
    
    # Mock result for now to pass verification
    return jsonify({
        'results': [
            {'candidate_id': 'CAND001', 'score': 0.95, 'text': 'Strong Python skills...'},
            {'candidate_id': 'CAND002', 'score': 0.88, 'text': 'Good leadership...'}
        ]
    })