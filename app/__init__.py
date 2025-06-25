from flask import Flask
from .models import db
from app.routes.pharmacy import pharmacy_bp
from app.routes.users import user_bp
import os
basedir = os.path.abspath(os.path.dirname(__file__))


# ps.不該放進create app的東西
# 1. db.create_all()
# 2. 匯入 JSON 
# 3. API call

def create_app(test_config=None):
    # 建立flask物件
    app = Flask(__name__)

    # 資料庫位置，存在根目錄，如果沒有建立，在create all會自動建立
    # 但create all不是寫在這裡，所以沒有db會報錯
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'phantom_mask.db')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../phantom_mask.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQL和Flask綁定
    db.init_app(app)

    # 註冊blueprint
    # 好處是如果有用url_prefix，在寫route那邊就可以不用再寫一次'/pharmacy'
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(user_bp)

    return app
