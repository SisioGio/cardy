from flask import Blueprint, jsonify
from models import Company
from app import db
bp = Blueprint('company', __name__, url_prefix='/companies')

@bp.route("/", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    return jsonify([{"id": c.id, "name": c.name, "slug": c.slug} for c in companies])
