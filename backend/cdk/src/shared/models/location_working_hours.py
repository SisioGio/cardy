from app import db
from sqlalchemy import Time
class LocationWorkingHours(db.Model):
    __tablename__ = 'location_working_hours'
    id = db.Column(db.String, primary_key=True)
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'))
    day_of_week = db.Column(db.String)
    open_time = db.Column(Time, nullable=True)
    close_time = db.Column(Time, nullable=True)
    is_closed = db.Column(db.Boolean, default=False)
