from flask import Flask
from flask_cors import CORS
from models import db
from database.config import DATABASE_URI
from routes.report_routes import report_bp
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# Configure database
# Set the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
# Register routes
app.register_blueprint(report_bp, url_prefix='/api/reports')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(host='0.0.0.0', port=5000)

