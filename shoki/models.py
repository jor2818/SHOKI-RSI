from shoki import db, bcrypt
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),nullable=False)
    hash_password = db.Column(db.String(60),nullable=False)
    rsis = db.relationship('Rsi', backref='user', lazy=True)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hash_password = bcrypt.generate_password_hash(password)
        
    def __repr__(self):
        return f"User({self.username},{self.email},{self.hash_password})"
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)
    
class Rsi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20),nullable=False)
    site_name = db.Column(db.String(20),nullable=False)
    direction = db.Column(db.String(30),nullable=False)
    vehicle_type = db.Column(db.String(30),nullable=False)
    addr1_og = db.Column(db.String(30),nullable=True)
    addr2_og = db.Column(db.String(30),nullable=True)
    addr3_og = db.Column(db.String(30),nullable=True)
    zone_og = db.Column(db.Integer,nullable=False)
    addr1_dn = db.Column(db.String(30),nullable=True)
    addr2_dn = db.Column(db.String(30),nullable=True)
    addr3_dn = db.Column(db.String(30),nullable=True)
    zone_dn = db.Column(db.Integer,nullable=False)
    trip_purpose = db.Column(db.String(30),nullable=False)
    passenger12 = db.Column(db.Integer,nullable=True)
    passenger34 = db.Column(db.String(30),nullable=True)
    passenger58 = db.Column(db.Integer,nullable=True)
    cargo_type = db.Column(db.String(30),nullable=True)
    cargo_weight = db.Column(db.String(30),nullable=True)
    income = db.Column(db.String(30),nullable=False)
    surveyor_name = db.Column(db.String(20),nullable=False)
    crated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    
    