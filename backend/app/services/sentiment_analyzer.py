from transformers import pipeline
import os
from typing import List, Dict, Optional

class SentimentAnalyzer:
    """Analyzes sentiment in employee communications"""
    
    def __init__(self):
        # Load sentiment analysis model (smaller for efficiency)
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU if GPU not available
            )
        except Exception as e:
            print(f"Warning: Could not load sentiment model: {e}")
            self.sentiment_pipeline = None
        
        # Keywords associated with exit intent
        self.exit_keywords = [
            'resign', 'quit', 'leave', 'exit', 'departure',
            'new opportunity', 'moving on', 'better offer',
            'relocation', 'career change', 'burnout',
            'frustrated', 'unhappy', 'dissatisfied',
            'underpaid', 'overworked', 'toxic'
        ]
        
        # Positive retention indicators
        self.retention_keywords = [
            'growth', 'opportunity', 'promotion', 'success',
            'appreciate', 'grateful', 'excited', 'motivated',
            'team', 'culture', 'belong', 'valued'
        ]
    
    def analyze_text(self, text):
        """
        Analyze sentiment of a single text.
        Returns dict with sentiment and score.
        """
        if not text or not isinstance(text, str):
            return {'sentiment': 'NEUTRAL', 'score': 0.5}
        
        try:
            if self.sentiment_pipeline:
                result = self.sentiment_pipeline(text[:512])[0]  # Limit to 512 chars
                
                sentiment_map = {
                    'POSITIVE': 'POSITIVE',
                    'NEGATIVE': 'NEGATIVE',
                    'NEUTRAL': 'NEUTRAL'
                }
                
                sentiment = sentiment_map.get(result['label'], 'NEUTRAL')
                score = result['score']
                
                return {
                    'sentiment': sentiment,
                    'score': round(score, 3)
                }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
        
        # Fallback: keyword-based sentiment
        return self._keyword_based_sentiment(text)
    
    def _keyword_based_sentiment(self, text):
        """
        Fallback sentiment analysis using keywords.
        """
        text_lower = text.lower()
        
        exit_score = sum(1 for keyword in self.exit_keywords if keyword in text_lower)
        retention_score = sum(1 for keyword in self.retention_keywords if keyword in text_lower)
        
        if exit_score > retention_score:
            return {'sentiment': 'NEGATIVE', 'score': 0.7}
        elif retention_score > exit_score:
            return {'sentiment': 'POSITIVE', 'score': 0.7}
        else:
            return {'sentiment': 'NEUTRAL', 'score': 0.5}
    
    def analyze_communications(self, communications: List[Dict]) -> Dict:
        """
        Analyze multiple communications and aggregate results.
        Returns dict with overall sentiment metrics.
        """
        if not communications:
            return {
                'overall_sentiment': 'NEUTRAL',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'average_score': 0.5,
                'exit_intent_score': 0,
                'exit_keywords_found': []
            }
        
        results = [self.analyze_text(comm.get('text', '')) for comm in communications]
        
        positive = sum(1 for r in results if r['sentiment'] == 'POSITIVE')
        negative = sum(1 for r in results if r['sentiment'] == 'NEGATIVE')
        neutral = sum(1 for r in results if r['sentiment'] == 'NEUTRAL')
        
        average_score = sum(r['score'] for r in results) / len(results) if results else 0.5
        
        # Calculate exit intent score
        exit_keywords_found = []
        for comm in communications:
            text_lower = comm.get('text', '').lower()
            for keyword in self.exit_keywords:
                if keyword in text_lower and keyword not in exit_keywords_found:
                    exit_keywords_found.append(keyword)
        
        # Exit intent score: higher negative sentiment + presence of exit keywords
        exit_intent_score = (negative / len(results) * 100) + (len(exit_keywords_found) * 5)
        exit_intent_score = min(exit_intent_score, 100)  # Cap at 100
        
        overall_sentiment = 'POSITIVE' if positive > negative else ('NEGATIVE' if negative > positive else 'NEUTRAL')
        
        return {
            'overall_sentiment': overall_sentiment,
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'total_communications': len(communications),
            'average_score': round(average_score, 3),
            'exit_intent_score': round(exit_intent_score, 2),
            'exit_keywords_found': exit_keywords_found,
            'negative_percentage': round((negative / len(results) * 100), 2)
        }
    
    def extract_concerns(self, communications: List[Dict]) -> List[str]:
        """
        Extract key concerns from communications.
        Returns list of concern themes.
        """
        concerns = []
        
        concern_keywords = {
            'compensation': ['salary', 'pay', 'wage', 'underpaid', 'raise'],
            'work_life_balance': ['hours', 'overtime', 'burnout', 'stress', 'exhausted'],
            'career': ['growth', 'advancement', 'promotion', 'development', 'stagnant'],
            'management': ['boss', 'manager', 'leadership', 'communication', 'micromanagement'],
            'team': ['team', 'conflict', 'culture', 'relationship', 'toxicity'],
            'role': ['responsibilities', 'expectations', 'clarity', 'purpose']
        }
        
        for comm in communications:
            text_lower = comm.get('text', '').lower()
            for concern_type, keywords in concern_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    if concern_type not in concerns:
                        concerns.append(concern_type)
        
        return concerns
