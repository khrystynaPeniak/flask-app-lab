from sqlalchemy.orm import backref
from app import db

class Cellphone(db.Model):
    __tablename__ = "cellphones"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    
   
    category_id = db.Column(db.Integer, db.ForeignKey('cellphone_categories.id'), nullable=True)
    category = db.relationship('CellphoneCategory', 
                             backref=backref("cellphones", lazy="dynamic"))
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    author = db.relationship('User', 
                           backref=backref("cellphones", lazy="dynamic"), 
                           lazy="joined")
    
    def __repr__(self):
        return f"Cellphone('{self.name}', '${self.price:.2f}')"

class CellphoneCategory(db.Model):
    __tablename__ = "cellphone_categories"  
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"CellphoneCategory('{self.category_name}')"