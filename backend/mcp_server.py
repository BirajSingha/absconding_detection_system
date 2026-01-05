#!/usr/bin/env python3
"""
MCP Server for Candidate Interview Analysis System
Provides tools and resources for absconding risk detection.
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from mcp.server.stdio import stdio_server
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.candidate import Candidate, InterviewAnalysis
from app.services.llm_analyzer import LLMAnalyzer

flask_app = create_app()
app_context = flask_app.app_context()
app_context.push()

server = Server("candidate-analysis-system")
llm_analyzer = LLMAnalyzer()

# Interview questions for MCP resource
INTERVIEW_QUESTIONS = [
    {"id": "q1", "text": "Why did you leave your last position?", "category": "job_stability"},
    {"id": "q2", "text": "How many jobs have you had in the last 5 years?", "category": "job_stability"},
    {"id": "q3", "text": "Where do you see yourself in 2 years?", "category": "commitment"},
    {"id": "q4", "text": "What are your long-term career goals?", "category": "commitment"},
    {"id": "q5", "text": "What would make you leave this role within the first year?", "category": "exit_intent"},
    {"id": "q6", "text": "What are the top 3 things you look for in an employer?", "category": "exit_intent"},
    {"id": "q7", "text": "How do you handle workplace conflicts?", "category": "behavioral"},
    {"id": "q8", "text": "Describe a time you felt undervalued at work. How did you respond?", "category": "behavioral"},
    {"id": "q9", "text": "If you received a better offer during probation, what would you do?", "category": "situational"},
    {"id": "q10", "text": "What concerns do you have about this position?", "category": "situational"}
]

@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="candidates://list",
            name="Candidate List",
            mimeType="application/json",
            description="List of all candidates and their statuses"
        ),
        Resource(
            uri="analysis://recent",
            name="Recent Analysis",
            mimeType="application/json",
            description="Recent interview analyses"
        ),
        Resource(
            uri="interview://questions",
            name="Interview Questions",
            mimeType="application/json",
            description="Absconding risk detection interview questions"
        ),
        Resource(
            uri="candidates://high-risk",
            name="High Risk Candidates",
            mimeType="application/json",
            description="Candidates with LOW fit category (high absconding risk)"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "candidates://list":
        candidates = Candidate.query.all()
        data = [c.to_dict() for c in candidates]
        return json.dumps(data, indent=2)
    elif uri == "analysis://recent":
        analyses = InterviewAnalysis.query.order_by(InterviewAnalysis.created_at.desc()).limit(10).all()
        data = [a.to_dict() for a in analyses]
        return json.dumps(data, indent=2)
    elif uri == "interview://questions":
        return json.dumps(INTERVIEW_QUESTIONS, indent=2)
    elif uri == "candidates://high-risk":
        candidates = Candidate.query.filter_by(fit_category='LOW').all()
        data = [c.to_dict() for c in candidates]
        return json.dumps(data, indent=2)
    else:
        return json.dumps({"error": "Resource not found"})

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_candidate_fit",
            description="Get fit score and analysis for a candidate",
            inputSchema={
                "type": "object",
                "properties": {
                    "candidate_id": {"type": "string"}
                },
                "required": ["candidate_id"]
            }
        ),
        Tool(
            name="analyze_interview_response",
            description="Analyze a candidate's interview response for absconding risk",
            inputSchema={
                "type": "object",
                "properties": {
                    "candidate_id": {"type": "string", "description": "Candidate ID"},
                    "question": {"type": "string", "description": "The interview question"},
                    "answer": {"type": "string", "description": "Candidate's answer"}
                },
                "required": ["candidate_id", "question", "answer"]
            }
        ),
        Tool(
            name="get_high_risk_candidates",
            description="Get list of candidates with high absconding risk",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "get_candidate_fit":
        candidate_id = arguments.get("candidate_id")
        candidate = Candidate.query.filter_by(candidate_id=candidate_id).first()
        if not candidate:
            return [TextContent(type="text", text="Candidate not found")]
            
        analysis = InterviewAnalysis.query.filter_by(candidate_id=candidate_id).order_by(InterviewAnalysis.created_at.desc()).first()
        
        result = {
            "name": candidate.name,
            "position": candidate.position_applied,
            "fit_score": analysis.fit_score if analysis else "N/A",
            "category": analysis.fit_category if analysis else "N/A",
            "summary": analysis.ai_summary if analysis else "No analysis found",
            "absconding_risk": "HIGH" if analysis and analysis.fit_category == "LOW" else "LOW"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "analyze_interview_response":
        candidate_id = arguments.get("candidate_id")
        question = arguments.get("question")
        answer = arguments.get("answer")
        
        # Format and analyze
        transcript = f"Q: {question}\nA: {answer}"
        result = llm_analyzer.analyze_transcript(transcript, "General")
        
        response = {
            "candidate_id": candidate_id,
            "fit_score": result["fit_score"],
            "fit_category": result["fit_category"],
            "tone": result["tone_analysis"],
            "summary": result["ai_summary"],
            "absconding_risk": "HIGH" if result["fit_category"] == "LOW" else "MODERATE" if result["fit_category"] == "MEDIUM" else "LOW"
        }
        return [TextContent(type="text", text=json.dumps(response, indent=2))]
    
    elif name == "get_high_risk_candidates":
        candidates = Candidate.query.filter_by(fit_category='LOW').all()
        result = [{
            "id": c.candidate_id,
            "name": c.name,
            "position": c.position_applied,
            "fit_score": c.fit_score,
            "status": c.status
        } for c in candidates]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
