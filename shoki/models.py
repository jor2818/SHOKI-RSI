from shoki import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),nullable=False)
    hash_password = db.Column(db.String(60),nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hash_password = bcrypt.generate_password_hash(password)
        
    def __repr__(self):
        return f"User({self.username},{self.email},{self.password})"
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)