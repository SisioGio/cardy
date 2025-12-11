from app import db

class LocationAbout(db.Model):
    __tablename__ = 'location_about'
    id = db.Column(db.String, primary_key=True)
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'))
    category = db.Column(db.String)
    key = db.Column(db.String)
    value = db.Column(db.Boolean)
    