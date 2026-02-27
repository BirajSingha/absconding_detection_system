from flask import Blueprint, request, jsonify
from app.services.rag_service import get_rag_service

bp = Blueprint('chat', __name__, url_prefix='/api/chat')
rag_service = get_rag_service()

@bp.route('/message', methods=['POST'])
def chat_message():
    """
    Handle chat messages from the candidate.
    Uses RAG to generate grounded responses from Offer FAQs/Policies.
    """
    data = request.json
    message = data.get('message')
    history = data.get('history', [])
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
        
    # Generate response using RAG (FAQ knowledge base)
    response_text = rag_service.generate_chat_response(message, history)
    
    return jsonify({
        'response': response_text
    })
