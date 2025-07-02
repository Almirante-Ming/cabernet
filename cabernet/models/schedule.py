from cabernet.config import db

class Schedule(db.Model):
    __tablename__='schedule'
    
    id=db.Column(db.Integer, primary_key=True, index=True)
    requerent_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lab_id=db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    course_id=db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    requerent = db.relationship('User', backref='schedule')
    lab = db.relationship('Lab', backref='schedule')
    course = db.relationship('Course', backref='schedule')
    