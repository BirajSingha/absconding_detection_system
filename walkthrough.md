# Walkthrough: Refactoring Interview Panel to Chatbot

I have successfully refactored the Absconding Detection System to replace the structured interview panel with a sophisticated HR Chatbot. This maintains the core AI analysis capabilities while significantly improving the candidate experience.

## Changes Implemented

### 1. Frontend: New Chat Interface

I replaced the rigid Q&A panel (`QuestionPanel`) with a modern, interactive `ChatInterface`.

- **Location**: `frontend/src/components/interview/ChatInterface.tsx`
- **Features**:
  - Real-time chat with an AI HR Assistant.
  - Neutral, polite responses grounded in company policy.
  - Automatic transcript accumulation.
  - Seamless integration with the existing `LiveAnalysis` panel.

### 2. Backend: Chat API & RAG

I implemented a new Chat API that uses Retrieval-Augmented Generation (RAG) to answer candidate queries.

- **New Route**: `POST /api/chat/message` (`backend/app/routes/chat.py`)
- **Knowledge Base Update**: Replaced generic interview knowledge with **Offer FAQs** and **Onboarding Policies**.
- **Service Update**: Added `generate_chat_response` to `RAGService` (`backend/app/services/rag_service.py`).
- **Data Seeding**: Updated `seed_vector_db.py` to populate the `hr_knowledge_base` with relevant FAQ content.

### 3. AI Analysis: Implicit Signal Detection

I updated the core AI analysis logic to handle unstructured chat transcripts instead of structured Q&A.

- **LLM Prompt Update**: Modified `LLMAnalyzer._create_analysis_prompt` (`backend/app/services/llm_analyzer.py`) to:
  - Analyze **implicit signals** (tone, repeated questions about notice period/bonds).
  - Map these signals to the original fit/risk dimensions (Stability, Commitment, Exit Intent).

## Verification Results

### Chatbot Interaction

- The chatbot successfully accepts user messages and returns RAG-grounded responses.
- It politely answers questions about "Joining Date", "Benefits", etc., without revealing its risk analysis function.

### AI Analysis Trigger

- Upon session completion (or manual "End Interview"), the full conversation transcript is sent to the AI.
- The AI correctly parses the transcript and generates a **Fit Score** and **Risk Assessment**.
- **High Risk** behavior (e.g., asking about breaking bonds) triggers the existing HR Alert workflow via n8n.

## How to Test

1. **Start the Backend**:
   ```bash
   python backend/run.py
   ```
2. **Launch the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
3. **Navigate to the Interview Page**:
   - Go to `http://localhost:3000/interview`
   - Enter your name and click "Start Chat Session".
4. **Interact with the Chatbot**:
   - Ask: "When is my joining date?" (Should see a policy-based answer).
   - Ask: "Can I break the bond?" (Should get a neutral answer, but trigger risk signals).
5. **End Session**:
   - Click "End Interview".
   - View the "Live Analysis" panel for the Fit Score and Alerts.
