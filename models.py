from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    folder_name = db.Column(db.String(50))
    storagesize = db.Column(db.String(20))
    auth = db.Column(db.String(50))
    permlevel = db.Column(db.Integer, default=0)
    
    def __init__(self, user_id, folder, storage, auth, perms = 0):
        self.user_id = user_id
        self.folder_name = folder 
        self.storagesize = storage
        self.auth = auth
        self.permlevel = perms
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    description = db.Column(db.String(500))
    webhook = db.Column(db.String(125))
    
    def __init__(self, name, description, webhook):
        self.name = name 
        self.description = description
        self.webhook = webhook
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()