from cabernet.config import db

class Course(db.Model):
    __tablename__='course'
    
    id=db.Column(db.Integer, primary_key=True, index=True)
    name=db.Column(db.String(50), nullable=False)
    period=db.Column(db.Integer, nullable=False)
    