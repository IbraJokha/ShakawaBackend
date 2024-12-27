from flask import Blueprint, request, jsonify
from models import db, Report

# Create a Blueprint for report routes
report_bp = Blueprint('reports', __name__)
#create report
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
            media_url=data.get('media_url'),
            phone_number=data.get('phone_number')  # Accept phone number
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
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 400

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
    try:
        db.session.delete(report)
        db.session.commit()
        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
