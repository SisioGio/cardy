from app import db

class Ingredients(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Numeric(10,2))
    item_id = db.Column(db.String, db.ForeignKey('item.id', ondelete='CASCADE'))
