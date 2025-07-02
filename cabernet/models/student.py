from cabernet.config import db

class Student(db.Model):
    __tablename__='student'
    
    id=db.Column(db.Integer, primary_key=True, index=True)
    name=db.Column(db.String(50), nullable=False)
    course_id=db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    course = db.relationship('Course', backref='students')