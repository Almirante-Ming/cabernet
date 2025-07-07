from cabernet.config import db, User_type

class User(db.Model):
    __tablename__='user'
    
    id=db.Column(db.Integer, primary_key=True, index=True)
    name=db.Column(db.String(50), nullable=False, unique=True)
    password_hash=db.Column(db.String(255), nullable=False)
    u_type=db.Column(db.Enum(User_type, name='user_type'), nullable=False, default=User_type.USER)