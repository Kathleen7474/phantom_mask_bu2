from app import create_app
from app.models import db

def create_database():
    app = create_app()
    # Flask 預設下不會主動知道你在哪個 App 環境，這行是用來告訴 Flask：接下來的程式碼是在這個 app 底下操作
    with app.app_context():
        # 就知道是建立app的資料庫
        db.create_all()
        print("Database created.")

if __name__ == "__main__":
    create_database()