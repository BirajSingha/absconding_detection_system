from textblob import TextBlob

class SentimentAnalyzer:
    """
    Service to analyze sentiment of interview transcripts using TextBlob.
    Provides simple polarity and subjectivity scores.
    """
    
    def __init__(self):
        pass
        
    def analyze_text(self, text):
        """
        Analyze text for sentiment polarity and subjectivity.
        """
        if not text:
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'NEUTRAL'}
            
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = 'POSITIVE'
        elif polarity < -0.1:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'
            
        return {
            'polarity': round(polarity, 2),
            'subjectivity': round(subjectivity, 2),
            'sentiment': sentiment
        }

    def analyze_segments(self, segments):
        """
        Analyze a list of transcript segments.
        """
        results = []
        total_polarity = 0
        
        for segment in segments:
            analysis = self.analyze_text(segment.get('text', ''))
            results.append({
                **segment,
                'sentiment_analysis': analysis
            })
            total_polarity += analysis['polarity']
            
        avg_polarity = total_polarity / len(segments) if segments else 0
        
        return {
            'segments': results,
            'overall_sentiment_score': round(avg_polarity, 2)
        }
