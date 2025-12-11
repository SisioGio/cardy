from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

from models import db
def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    CORS(app, origins=["http://localhost:3000"])
    # app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)

    # Import models AFTER db.init_app(app)
    from models import Company, Location, Item

    # Import blueprints
    from routes.company_routes import bp as company_bp
    from routes.location_routes import bp as location_bp
    from routes.item_routes import bp as item_bp
    from routes.utils_routes import bp as utils_bp
    # Register blueprints
    app.register_blueprint(company_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(utils_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
       
        db.create_all()
    app.run(debug=True)
