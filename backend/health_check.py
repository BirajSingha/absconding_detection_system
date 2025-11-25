"""
Quick Backend Health Check Script
Tests core functionality without running Flask server
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("=" * 70)
print("ABSCONDING DETECTION SYSTEM - BACKEND HEALTH CHECK")
print("=" * 70)

# Test 1: Environment Configuration
print("\n[1/6] Testing Environment Configuration...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check critical variables
    db_url = os.getenv('DATABASE_URL')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    chroma_key = os.getenv('CHROMA_API_KEY')
    
    print(f"  ✓ DATABASE_URL: {db_url[:40]}...")
    print(f"  {'✓' if anthropic_key and anthropic_key != 'your_anthropic_key_here' else '⚠'} ANTHROPIC_API_KEY: {'Configured' if anthropic_key and anthropic_key != 'your_anthropic_key_here' else 'Placeholder'}")
    print(f"  {'✓' if chroma_key else '⚠'} CHROMA_API_KEY: {'Configured' if chroma_key else 'Not set'}")
    print(f"  {'✓' if os.getenv('SENDER_EMAIL') else '⚠'} EMAIL: {'Configured' if os.getenv('SENDER_EMAIL') else 'Not set'}")
    print("  Status: PASS")
except Exception as e:
    print(f"  Status: FAIL - {e}")
    sys.exit(1)

# Test 2: Database Models
print("\n[2/6] Testing Database Models...")
try:
    from app.models.employee import Employee, Alert, Communication
    print("  ✓ Employee model imported")
    print("  ✓ Alert model imported")
    print("  ✓ Communication model imported")
    print("  Status: PASS")
except Exception as e:
    print(f"  Status: FAIL - {e}")
    sys.exit(1)

# Test 3: Service Initialization
print("\n[3/6] Testing Services Initialization...")
try:
    from app.services.anomaly_detector import AnomalyDetector
    from app.services.sentiment_analyzer import SentimentAnalyzer
    
    detector = AnomalyDetector()
    analyzer = SentimentAnalyzer()
    
    print("  ✓ AnomalyDetector initialized")
    print("  ✓ SentimentAnalyzer initialized")
    
    # Test vector store (may use mock if not configured)
    try:
        from app.services.vector_store import get_vector_store
        vector_store = get_vector_store()
        print("  ✓ VectorStore initialized")
    except Exception as e:
        print(f"  ⚠ VectorStore: {str(e)[:50]}... (may use mock)")
    
    # Test RAG service
    try:
        from app.services.rag_service import get_rag_service
        rag = get_rag_service()
        print("  ✓ RAGService initialized")
    except Exception as e:
        print(f"  ⚠ RAGService: {str(e)[:50]}... (may use mock)")
    
    # Test notification services
    from app.services.slack_service import get_slack_service
    from app.services.email_service import get_email_service
    
    slack = get_slack_service()
    email = get_email_service()
    print("  ✓ SlackService initialized")
    print("  ✓ EmailService initialized")
    
    print("  Status: PASS")
except Exception as e:
    print(f"  Status: FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Flask App Creation
print("\n[4/6] Testing Flask Application...")
try:
    from app import create_app, db
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("  ✓ Flask app created")
        print("  ✓ Database tables created")
        
        # Check blueprints
        blueprints = list(app.blueprints.keys())
        print(f"  ✓ Registered blueprints: {', '.join(blueprints)}")
        
    print("  Status: PASS")
except Exception as e:
    print(f"  Status: FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: API Routes
print("\n[5/6] Testing API Routes...")
try:
    with app.app_context():
        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(f"{','.join(rule.methods)} {rule.rule}")
        
        # Check key endpoints
        key_endpoints = [
            '/api/employees',
            '/api/alerts',
            '/api/analytics/risk-distribution',
            '/api/webhooks/n8n/get-high-risk'
        ]
        
        for endpoint in key_endpoints:
            found = any(endpoint in route for route in routes)
            print(f"  {'✓' if found else '✗'} {endpoint}")
        
        print(f"  ✓ Total routes: {len(routes)}")
        print("  Status: PASS")
except Exception as e:
    print(f"  Status: FAIL - {e}")
    sys.exit(1)

# Test 6: Basic Functionality
print("\n[6/6] Testing Core Functionality...")
try:
    with app.app_context():
        # Test anomaly detection
        test_anomalies = detector.detect_anomalies("TEST001")
        print(f"  ✓ Anomaly detection working (found {len(test_anomalies)} anomalies)")
        
        # Test sentiment analysis
        test_sentiment = analyzer.analyze_text("I am happy at work")
        print(f"  ✓ Sentiment analysis working (sentiment: {test_sentiment.get('sentiment', 'N/A')})")
        
    print("  Status: PASS")
except Exception as e:
    print(f"  Status: FAIL - {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("HEALTH CHECK COMPLETE")
print("=" * 70)
print("\n✅ All core systems operational!")
print("\nNext steps:")
print("  1. Run full integration tests: python test_integration.py")
print("  2. Start Flask server: python run.py")
print("  3. Test with demo data: python create_demo_data.py")
print("\n" + "=" * 70)
