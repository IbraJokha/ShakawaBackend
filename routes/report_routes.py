from flask import Blueprint, request, jsonify
from models import db, Report

# Create a Blueprint for report routes
report_bp = Blueprint('reports', __name__)

# Helper function for authentication (placeholder)
def authenticate_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != "Bearer YOUR_SECRET_TOKEN":  # Replace with actual logic
        return False
    return True

# Middleware to require authentication (except for certain routes)
@report_bp.before_request
def require_auth():
    exempt_routes = [
        ('reports.create_report', 'POST'),
        ('reports.get_reports_by_phone', 'GET'),
    ]
    if (request.endpoint, request.method) not in exempt_routes:
        if not authenticate_request():
            return jsonify({'error': 'Unauthorized'}), 401

# Create a new report
@report_bp.route('/', methods=['POST'])
def create_report():
    data = request.json
    try:
        report = Report(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            gps_location=data.get('gps_location'),
            manual_location=data.get('manual_location'),
            media_url=data.get('media_url')
        )
        db.session.add(report)
        db.session.commit()
        return jsonify({'message': 'Report created successfully!', 'report': report.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Fetch all reports
@report_bp.route('/', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    result = [
        {
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'category': report.category,
            'gps_location': report.gps_location,
            'manual_location': report.manual_location,
            'media_url': report.media_url,
            'created_at': report.created_at
        } for report in reports
    ]
    return jsonify(result), 200

# Fetch reports by phone number
@report_bp.route('/phone/<string:phone_number>', methods=['GET'])
def get_reports_by_phone(phone_number):
    reports = Report.query.filter_by(phone_number=phone_number).all()
    result = [
        {
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'category': report.category,
            'gps_location': report.gps_location,
            'manual_location': report.manual_location,
            'media_url': report.media_url,
            'created_at': report.created_at
        } for report in reports
    ]
    return jsonify(result), 200

# Fetch a single report by ID
@report_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    report = Report.query.get(report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    return jsonify({
        'id': report.id,
        'title': report.title,
        'description': report.description,
        'category': report.category,
        'gps_location': report.gps_location,
        'manual_location': report.manual_location,
        'media_url': report.media_url,
        'created_at': report.created_at
    }), 200

# Delete a report
@report_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    report = Report.query.get(report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Report deleted successfully'}), 200
