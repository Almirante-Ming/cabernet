from cabernet.config import db

class Lab(db.Model):
    __tablename__='lab'
    
    id=db.Column(db.Integer, primary_key=True, index=True)
    name=db.Column(db.String(50), nullable=False)