from flask_sqlalchemy import SQLAlchemy
from datetime import time, datetime, timezone

db = SQLAlchemy()

class Pharmacy(db.Model):
    __tablename__ = 'pharmacies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cash_balance = db.Column(db.Float, nullable=False)
    # all delete orphan是指如果有pharmacy被刪除了，連結的OpeningHour也一起刪除（這裡好像用不到）
    opening_hours = db.relationship('OpeningHour', backref='pharmacy', cascade='all, delete-orphan')

class OpeningHour(db.Model):
    __tablename__ = 'opening_hours'
    id = db.Column(db.Integer, primary_key=True)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False)
    day_of_week = db.Column(db.String, nullable=False)  # 'Mon', 'Tue', ...
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)

class Mask(db.Model):
    __tablename__ = 'masks'
    id = db.Column(db.Integer, primary_key=True)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Float, nullable=False)
    # 如果pharmacy使用pharmacy.mask就可以取用所有他擁有的masks（雙向都可以）
    # lazy是指用到的時候才去join，如果一開始就要join可以lazy = "joined"
    pharmacy = db.relationship('Pharmacy', backref=db.backref('masks', lazy=True))

    # debug可以用
    # def __repr__(self):
    #     return f"<Mask {self.name} (${self.price}) x{self.stock_quantity}>"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cash_balance = db.Column(db.Float, nullable=False)
    purchase_histories = db.relationship('PurchaseHistory', backref='user', cascade='all, delete-orphan')

class PurchaseHistory(db.Model):
    __tablename__ = 'purchase_histories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pharmacy_id = db.Column(db.Integer, db.ForeignKey('pharmacies.id'), nullable=False)
    mask_name = db.Column(db.String, nullable=False)  # 字串存口罩名稱

    # 單價（會浮動）
    transaction_amount = db.Column(db.Float, nullable=False)
    transaction_quantity = db.Column(db.Integer, nullable=False)
    transaction_datetime = db.Column(db.DateTime, nullable=False)

    pharmacy = db.relationship('Pharmacy', backref='purchase_histories')
