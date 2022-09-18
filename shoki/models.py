from shoki import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(60),nullable=False)
    
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
        
    def __repr__(self):
        return f"User({self.username},{self.email},{self.password})"