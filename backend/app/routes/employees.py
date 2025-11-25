from flask import Blueprint, request, jsonify
from app.models.employee import Employee
from app import db

bp = Blueprint('employees', __name__, url_prefix='/api/employees')

@bp.route('', methods=['GET'])
def list_employees():
    """Get all employees"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Employee.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'employees': [emp.to_dict() for emp in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get employee details"""
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    return jsonify(employee.to_dict())

@bp.route('', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.json
    
    # Validate required fields
    required_fields = ['employee_id', 'name', 'role', 'department']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if employee already exists
    if Employee.query.filter_by(employee_id=data['employee_id']).first():
        return jsonify({'error': 'Employee already exists'}), 409
    
    employee = Employee(
        employee_id=data['employee_id'],
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        role=data['role'],
        department=data['department'],
        tenure_years=data.get('tenure_years', 0),
        manager_id=data.get('manager_id'),
        manager_name=data.get('manager_name'),
        employment_status=data.get('employment_status', 'ACTIVE'),
        productivity_score=data.get('productivity_score', 100),
        attendance_percentage=data.get('attendance_percentage', 100),
        performance_rating=data.get('performance_rating', 3.0)
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify(employee.to_dict()), 201

@bp.route('/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update employee information"""
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    data = request.json
    
    # Update fields
    if 'name' in data:
        employee.name = data['name']
    if 'email' in data:
        employee.email = data['email']
    if 'phone' in data:
        employee.phone = data['phone']
    if 'role' in data:
        employee.role = data['role']
    if 'department' in data:
        employee.department = data['department']
    if 'tenure_years' in data:
        employee.tenure_years = data['tenure_years']
    if 'manager_id' in data:
        employee.manager_id = data['manager_id']
    if 'manager_name' in data:
        employee.manager_name = data['manager_name']
    if 'employment_status' in data:
        employee.employment_status = data['employment_status']
    if 'productivity_score' in data:
        employee.productivity_score = data['productivity_score']
    if 'attendance_percentage' in data:
        employee.attendance_percentage = data['attendance_percentage']
    if 'performance_rating' in data:
        employee.performance_rating = data['performance_rating']
    
    db.session.commit()
    
    return jsonify(employee.to_dict())

@bp.route('/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    db.session.delete(employee)
    db.session.commit()
    
    return jsonify({'message': 'Employee deleted successfully'})

@bp.route('/<employee_id>/metrics', methods=['PUT'])
def update_metrics(employee_id):
    """Update employee performance metrics"""
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    data = request.json
    
    if 'productivity_score' in data:
        employee.productivity_score = data['productivity_score']
    if 'attendance_percentage' in data:
        employee.attendance_percentage = data['attendance_percentage']
    if 'performance_rating' in data:
        employee.performance_rating = data['performance_rating']
    
    db.session.commit()
    
    return jsonify(employee.to_dict())
