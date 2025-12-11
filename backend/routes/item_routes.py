from flask import Blueprint, jsonify
from models import Item
from models import Location

bp = Blueprint('item', __name__, url_prefix='/items')

@bp.route("/<location_id>", methods=["GET"])
def get_items(location_id):
    location = Location.query.filter_by(slug=location_id).first()
    if not location:
        return jsonify({"error": "Location not found"}), 404
    items = Item.query.filter_by(location_id=location.slug).all()
    return jsonify([{"id": i.id, "name": i.name, "price": str(i.price)} for i in items])
