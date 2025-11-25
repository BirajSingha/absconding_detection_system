#!/usr/bin/env python3
"""
MCP Server for Absconding Detection System

This server exposes employee data, alerts, and analytics as MCP resources
and provides tools for AI assistants to interact with the HR system.
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.employee import Employee, Alert
from app.services.anomaly_detector import AnomalyDetector
from app.services.sentiment_analyzer import SentimentAnalyzer

# Initialize Flask app context
flask_app = create_app()
app_context = flask_app.app_context()
app_context.push()

# Initialize services
anomaly_detector = AnomalyDetector()
sentiment_analyzer = SentimentAnalyzer()

# Create MCP server
server = Server("absconding-detection-system")

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources in the absconding detection system"""
    return [
        Resource(
            uri="absconding://employees/list",
            name="Employee List",
            mimeType="application/json",
            description="List of all employees with their current status and metrics"
        ),
        Resource(
            uri="absconding://alerts/active",
            name="Active Alerts",
            mimeType="application/json",
            description="Currently active high-risk alerts"
        ),
        Resource(
            uri="absconding://analytics/risk-distribution",
            name="Risk Distribution",
            mimeType="application/json",
            description="Distribution of employees across risk levels"
        ),
        Resource(
            uri="absconding://analytics/department-stats",
            name="Department Statistics",
            mimeType="application/json",
            description="Risk and performance statistics by department"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource"""
    
    if uri == "absconding://employees/list":
        employees = Employee.query.all()
        data = [emp.to_dict() for emp in employees]
        return json.dumps(data, indent=2)
    
    elif uri == "absconding://alerts/active":
        alerts = Alert.query.filter(
            Alert.status.in_(['OPEN', 'ACKNOWLEDGED']),
            Alert.risk_level.in_(['HIGH', 'CRITICAL'])
        ).order_by(Alert.risk_score.desc()).all()
        
        result = []
        for alert in alerts:
            employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
            result.append({
                'alert': alert.to_dict(),
                'employee': employee.to_dict() if employee else None
            })
        return json.dumps(result, indent=2)
    
    elif uri == "absconding://analytics/risk-distribution":
        risk_counts = {
            'CRITICAL': Alert.query.filter_by(risk_level='CRITICAL').count(),
            'HIGH': Alert.query.filter_by(risk_level='HIGH').count(),
            'MEDIUM': Alert.query.filter_by(risk_level='MEDIUM').count(),
            'LOW': Alert.query.filter_by(risk_level='LOW').count()
        }
        return json.dumps(risk_counts, indent=2)
    
    elif uri == "absconding://analytics/department-stats":
        from sqlalchemy import func
        departments = db.session.query(
            Employee.department,
            func.count(Employee.id).label('total'),
            func.avg(Employee.productivity_score).label('avg_productivity'),
            func.avg(Employee.attendance_percentage).label('avg_attendance')
        ).group_by(Employee.department).all()
        
        result = []
        for dept in departments:
            result.append({
                'department': dept[0],
                'total_employees': dept[1],
                'avg_productivity': float(dept[2]) if dept[2] else 0,
                'avg_attendance': float(dept[3]) if dept[3] else 0
            })
        return json.dumps(result, indent=2)
    
    else:
        return json.dumps({"error": "Resource not found"})

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="analyze_employee_risk",
            description="Analyze absconding risk for a specific employee",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID to analyze"
                    }
                },
                "required": ["employee_id"]
            }
        ),
        Tool(
            name="get_employee_details",
            description="Get detailed information about an employee including recent alerts",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID to retrieve"
                    }
                },
                "required": ["employee_id"]
            }
        ),
        Tool(
            name="update_employee_metrics",
            description="Update performance metrics for an employee",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID"
                    },
                    "productivity_score": {
                        "type": "number",
                        "description": "Productivity score (0-100)"
                    },
                    "attendance_percentage": {
                        "type": "number",
                        "description": "Attendance percentage (0-100)"
                    },
                    "performance_rating": {
                        "type": "number",
                        "description": "Performance rating (0-4)"
                    }
                },
                "required": ["employee_id"]
            }
        ),
        Tool(
            name="get_high_risk_employees",
            description="Get list of employees currently at high risk of absconding",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of employees to return",
                        "default": 10
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a tool"""
    
    if name == "analyze_employee_risk":
        employee_id = arguments.get("employee_id")
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        
        if not employee:
            return [TextContent(type="text", text=f"Employee {employee_id} not found")]
        
        # Detect anomalies
        anomalies = anomaly_detector.detect_anomalies(employee_id)
        risk_score = anomaly_detector.calculate_risk_score(anomalies)
        
        result = {
            "employee_id": employee_id,
            "employee_name": employee.name,
            "department": employee.department,
            "risk_score": risk_score,
            "anomalies": anomalies,
            "recommendation": "HIGH PRIORITY - Immediate intervention needed" if risk_score >= 60 else "Monitor closely"
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_employee_details":
        employee_id = arguments.get("employee_id")
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        
        if not employee:
            return [TextContent(type="text", text=f"Employee {employee_id} not found")]
        
        alerts = Alert.query.filter_by(employee_id=employee_id).order_by(Alert.created_at.desc()).limit(5).all()
        
        result = {
            "employee": employee.to_dict(),
            "recent_alerts": [alert.to_dict() for alert in alerts]
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "update_employee_metrics":
        employee_id = arguments.get("employee_id")
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        
        if not employee:
            return [TextContent(type="text", text=f"Employee {employee_id} not found")]
        
        if "productivity_score" in arguments:
            employee.productivity_score = arguments["productivity_score"]
        if "attendance_percentage" in arguments:
            employee.attendance_percentage = arguments["attendance_percentage"]
        if "performance_rating" in arguments:
            employee.performance_rating = arguments["performance_rating"]
        
        db.session.commit()
        
        return [TextContent(type="text", text=f"Updated metrics for {employee.name}")]
    
    elif name == "get_high_risk_employees":
        limit = arguments.get("limit", 10)
        
        alerts = Alert.query.filter(
            Alert.risk_level.in_(['HIGH', 'CRITICAL']),
            Alert.status.in_(['OPEN', 'ACKNOWLEDGED'])
        ).order_by(Alert.risk_score.desc()).limit(limit).all()
        
        result = []
        for alert in alerts:
            employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
            if employee:
                result.append({
                    "employee_id": employee.employee_id,
                    "name": employee.name,
                    "department": employee.department,
                    "risk_score": alert.risk_score,
                    "risk_level": alert.risk_level
                })
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
