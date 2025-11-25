from flask import Blueprint, request, jsonify
from app.services.vector_store import get_vector_store
from app.services.seed_vector_db import seed_all

bp = Blueprint('vector_db', __name__, url_prefix='/api/vector-db')

vector_store = get_vector_store()

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get vector database statistics"""
    stats = vector_store.get_collection_stats()
    return jsonify(stats)

@bp.route('/search/knowledge', methods=['POST'])
def search_knowledge():
    """Search knowledge base"""
    data = request.json
    query = data.get('query', '')
    n_results = data.get('n_results', 5)
    
    results = vector_store.search_knowledge(query, n_results)
    return jsonify({'results': results})

@bp.route('/search/cases', methods=['POST'])
def search_cases():
    """Search historical cases"""
    data = request.json
    query = data.get('query', '')
    n_results = data.get('n_results', 5)
    
    results = vector_store.search_similar_cases(query, n_results)
    return jsonify({'results': results})

@bp.route('/search/communications/<employee_id>', methods=['GET'])
def search_communications(employee_id):
    """Search employee communications"""
    query = request.args.get('query')
    n_results = int(request.args.get('n_results', 10))
    
    results = vector_store.search_employee_communications(
        employee_id, 
        query, 
        n_results
    )
    return jsonify({'results': results})

@bp.route('/seed', methods=['POST'])
def seed_database():
    """Seed vector database with initial data"""
    try:
        seed_all()
        return jsonify({'message': 'Vector database seeded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add/knowledge', methods=['POST'])
def add_knowledge():
    """Add document to knowledge base"""
    data = request.json
    
    doc_id = data.get('id')
    content = data.get('content')
    metadata = data.get('metadata', {})
    
    if not doc_id or not content:
        return jsonify({'error': 'Missing required fields'}), 400
    
    vector_store.add_knowledge_document(doc_id, content, metadata)
    return jsonify({'message': 'Document added successfully'})