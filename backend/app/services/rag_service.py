from google import genai
import os
from app.services.vector_store import get_vector_store
import json

class RAGService:
    """RAG Service using Vector Database for context retrieval"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.0-flash-lite-preview-02-05'
        self.vector_store = get_vector_store()
    
    def analyze_risk(self, employee_data, anomalies, sentiment_data):
        """Analyze risk using RAG with vector database"""
        
        # 1. Create query for similar cases
        query_text = self._create_search_query(employee_data, anomalies, sentiment_data)
        
        # 2. Retrieve relevant context from vector DB
        similar_cases = self.vector_store.search_similar_cases(query_text, n_results=3)
        retention_strategies = self.vector_store.search_knowledge(
            "retention strategies for " + employee_data.get('role', ''),
            n_results=2
        )
        exit_indicators = self.vector_store.search_knowledge(
            "exit indicators and patterns",
            n_results=2
        )
        
        # 3. Build context from vector search results
        context = self._build_context(similar_cases, retention_strategies, exit_indicators)
        
        # 4. Get employee communications history
        employee_comms = self.vector_store.search_employee_communications(
            employee_data.get('employee_id'),
            query="negative sentiment or exit intent",
            n_results=5
        )
        
        # 5. Create prompt with context
        prompt = self._create_analysis_prompt(
            employee_data, 
            anomalies, 
            sentiment_data,
            context,
            employee_comms
        )
        
        # 6. Get AI analysis
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            response_text = response.text
            
            # Extract JSON from response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            result = json.loads(response_text.strip())
            
            # Add source citations
            result['sources'] = {
                'similar_cases_count': len(similar_cases),
                'knowledge_docs_used': len(retention_strategies) + len(exit_indicators),
                'communications_analyzed': len(employee_comms)
            }
            
            return result
        
        except Exception as e:
            print(f"RAG Error: {e}")
            return self._fallback_analysis(anomalies, sentiment_data)
    
    def _create_search_query(self, employee_data, anomalies, sentiment_data):
        """Create query for vector similarity search"""
        
        indicators = []
        for anomaly in anomalies:
            indicators.append(f"{anomaly['type']}: {anomaly.get('change', anomaly.get('drop', ''))}")
        
        if sentiment_data:
            indicators.append(f"Sentiment: {sentiment_data.get('overall_sentiment')}")
            indicators.append(f"Exit Intent: {sentiment_data.get('exit_intent_score')}%")
        
        query = f"""
        Employee in {employee_data.get('role')} role with {employee_data.get('tenure_years')} years tenure
        showing following indicators: {', '.join(indicators)}
        """
        
        return query
    
    def _build_context(self, similar_cases, retention_strategies, exit_indicators):
        """Build context from vector search results"""
        
        context = "### Similar Historical Cases:\n\n"
        for i, case in enumerate(similar_cases, 1):
            context += f"Case {i}:\n{case['content']}\n\n"
        
        context += "\n### Retention Strategies:\n\n"
        for strategy in retention_strategies:
            context += f"{strategy['content']}\n\n"
        
        context += "\n### Exit Indicators Knowledge:\n\n"
        for indicator in exit_indicators:
            context += f"{indicator['content']}\n\n"
        
        return context
    
    def _create_analysis_prompt(self, employee_data, anomalies, sentiment_data, 
                                context, employee_comms):
        """Create analysis prompt with context"""
        
        comms_summary = "\n".join([
            f"- [{c['metadata'].get('source')}] {c['content'][:100]}..." 
            for c in employee_comms[:3]
        ])
        
        prompt = f"""You are an expert HR analyst. Analyze this employee's absconding risk.

## Employee Profile:
- Name: {employee_data['name']}
- Role: {employee_data['role']}
- Department: {employee_data['department']}
- Tenure: {employee_data['tenure_years']} years

## Behavioral Anomalies Detected:
{json.dumps(anomalies, indent=2)}

## Sentiment Analysis:
{json.dumps(sentiment_data, indent=2)}

## Recent Communications (Last 5):
{comms_summary}

## Historical Context & Knowledge Base:
{context}

Based on the historical cases and knowledge base, provide a JSON response with:
{{
  "exit_probability": <number 0-100>,
  "confidence_level": "<HIGH|MEDIUM|LOW>",
  "key_indicators": [<list of most critical indicators>],
  "timeline_estimate": "<estimated time until potential resignation>",
  "recommended_actions": [<prioritized list of actions>],
  "similar_cases_insight": "<brief summary of what worked in similar cases>",
  "summary": "<2-3 sentence analysis>"
}}

Be specific and actionable. Consider the success/failure patterns from historical cases.
"""
        
        return prompt
    
    def _fallback_analysis(self, anomalies, sentiment_data):
        """Fallback analysis if AI fails"""
        risk_score = len(anomalies) * 20
        if sentiment_data:
            risk_score = (risk_score + sentiment_data.get('exit_intent_score', 0)) / 2
        
        return {
            'exit_probability': min(risk_score, 100),
            'confidence_level': 'MEDIUM',
            'key_indicators': [a['type'] for a in anomalies],
            'timeline_estimate': '2-4 weeks',
            'recommended_actions': ['Immediate HR review', 'Manager intervention'],
            'summary': 'AI analysis unavailable, using rule-based assessment',
            'sources': {'error': 'AI service unavailable'}
        }
    
    def store_case_outcome(self, alert_data, outcome, success):
        """Store case outcome in vector DB for future learning"""
        case_data = {
            'employee_name': alert_data['employee_name'],
            'role': alert_data['role'],
            'department': alert_data['department'],
            'tenure_years': alert_data['tenure_years'],
            'indicators': alert_data['behavioral_indicators'],
            'intervention': alert_data.get('intervention_taken'),
            'outcome': outcome,
            'success': success,
            'timestamp': alert_data['timestamp']
        }
        
        case_id = f"case_{alert_data['employee_id']}_{alert_data['timestamp']}"
        self.vector_store.add_historical_case(case_id, case_data)

# Singleton instance
_rag_service_instance = None

def get_rag_service() -> RAGService:
    """Get RAGService singleton instance"""
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance