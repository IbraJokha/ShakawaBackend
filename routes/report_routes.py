from flask import Blueprint, request, jsonify
from models import db, Report
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import DATABASE_URI

# Create a Blueprint for report routes
report_bp = Blueprint('reports', __name__)
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
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
def get_reports():
    """
    Get all reports or filter by phone number if provided.
    """
    try:
        phone_number = request.args.get('phone_number')  # Get phone_number from query params
        if phone_number:
            reports = session.query(Report).filter_by(phone_number=phone_number).all()
        else:
            reports = session.query(Report).all()
        
        # Convert reports to dict format
        return jsonify([report.to_dict() for report in reports]), 200
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify({"error": "Unable to fetch reports"}), 500

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
