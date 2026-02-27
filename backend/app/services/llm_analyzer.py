# from google import genai  <-- Moved to local scope
import os
import json
import logging

class LLMAnalyzer:
    """
    Service to analyze interview transcripts for absconding risk detection.
    Uses Google's Gemini AI (google-genai SDK) to evaluate candidate responses.
    """
    
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        from google import genai  # Lazy import
        if not api_key:
            logging.warning("GEMINI_API_KEY not found. LLMAnalyzer will fail.")
        else:
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'models/gemini-2.5-flash'
        
    def analyze_transcript(self, text, position):
        """
        Analyzes the transcript to determine fit for the position.
        Returns a dictionary with scores and insights.
        """
        if not text:
            return self._fallback_analysis("No text provided")
            
        import time
        
        max_retries = 3
        retry_delay = 2 # start with 2 seconds
        
        for attempt in range(max_retries):
            try:
                prompt = self._create_analysis_prompt(text, position)
                
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
                
                analysis = json.loads(response_text.strip())
                return analysis
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "ResourceExhausted" in error_str:
                    if attempt < max_retries - 1:
                        logging.warning(f"Rate limit hit (429). Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2 # Exponential backoff
                        continue
                
                # If not a retryable error or max retries reached:
                print(f"CRITICAL LLM ERROR: {e}") 
                logging.error(f"LLM Analysis failed: {e}")
                return self._fallback_analysis(str(e))

    def _create_analysis_prompt(self, text, position):
        return f"""
        You are an Expert Interview Psychologist and HR Data Analyst. 
        Analyze the following Chatbot Conversation Transcript between a candidate and an AI HR Assistant.
        Position: "{position}".
        
        Transcript:
        "{text}"
        
        Your goal is to evaluate the candidate's psychological profile, specifically focusing on "Absconding Risk" (likelihood of leaving abruptly).
        The candidate believes they are just asking HR queries, so their guard is down.
        
        CRITICAL INSTRUCTION: Analyze IMPLICIT SIGNALS from the conversation:
        1. Repeated clarification on "Joining Date" or "Notice Period" -> May imply holding other offers (High Risk).
        2. Questions about "Bond breaking", "Exit process", or "Moonlighting" -> High Risk of absconding/moonlighting.
        3. Excessive focus on "Perks/Benefits/Leaves" vs "Role/Responsibilities" -> Transactional mindset.
        4. Hesitation or postponement language -> Possible counter-offer negotiation.
        5. Tone: Impatient, demanding, or evasive vs. Professional and inquiring.
        
        Map these implicit signals to the exact same dimensions as a structured interview:
        - Stability: Does the candidate seem settled or looking for a quick switch?
        - Commitment: Are they asking about long-term growth or short-term gains?
        - Exit Intent: Are they already planning their exit?
        
        Provide the output EXCLUSIVELY as a valid JSON object with the following structure:
        {{
            "fit_score": <int 0-100>,
            "fit_category": "<EXCELLENT|HIGH|MEDIUM|LOW>",
            "confidence_score": <float 0-10>,
            "tone_analysis": {{
                "confidence": <float 0-10>,
                "nervousness": <float 0-10>,
                "professionalism": <float 0-10>,
                "tone_label": "<Confident|Hesitant|Defensive|Neutral|Enthusiastic>"
            }},
            "behavioral_traits": {{
                "leadership": <float 1-10>,
                "teamwork": <float 1-10>,
                "problem_solving": <float 1-10>,
                "commitment": <float 1-10>,
                "stability": <float 1-10>
            }},
            "ai_summary": "<One sentence summary of the candidate's profile and risk level based on chat signals>",
            "recommendations": ["<Rec 1>", "<Rec 2>", "<Rec 3>"]
        }}
        """

    def _fallback_analysis(self, error_msg):
        """Return a safe fallback if AI fails"""
        return {
            'fit_score': 0,
            'fit_category': 'UNKNOWN',
            'confidence_score': 0,
            'tone_analysis': {
                'confidence': 0, 'nervousness': 0, 
                'professionalism': 0, 'tone_label': 'Error'
            },
            'behavioral_traits': {
                'leadership': 0, 'teamwork': 0, 
                'problem_solving': 0, 'commitment': 0, 
                'stability': 0
            },
            'ai_summary': f"Analysis failed due to system error: {error_msg}",
            'recommendations': ["Manual retry required"]
        }
