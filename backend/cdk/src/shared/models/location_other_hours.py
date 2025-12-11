from app import db
from sqlalchemy import Time
class LocationOtherHours(db.Model):
    __tablename__ = 'location_other_hours'
    id = db.Column(db.String, primary_key=True)
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'))
    category = db.Column(db.String)
    day_of_week = db.Column(db.String)
    open_time = db.Column(Time, nullable=True)
    close_time = db.Column(Time, nullable=True)
    is_closed = db.Column(db.Boolean, default=False)
