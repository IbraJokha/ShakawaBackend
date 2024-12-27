from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    gps_location = db.Column(db.String(100), nullable=True)
    manual_location = db.Column(db.String(100), nullable=True)
    media_url = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)  # Add this
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Report {self.title}>"
