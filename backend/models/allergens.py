from app import db

class Allergens(db.Model):
    __tablename__ = 'allergens'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    item_id = db.Column(db.String, db.ForeignKey('item.id', ondelete='CASCADE'))
