# load_users.py
import json
from datetime import datetime
from app import create_app
from app.models import db, User, PurchaseHistory, Pharmacy

def load_users(json_path):
    app = create_app()
    with app.app_context():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for u in data:
            user = User(
                name=u['name'],
                cash_balance=u['cashBalance']
            )
            db.session.add(user)
            db.session.flush()  # 讓 user.id 有值

            for ph in u.get('purchaseHistories', []):
                # 透過pharmacyName查pharmacy.id
                pharmacy = Pharmacy.query.filter_by(name=ph['pharmacyName']).first()
                if not pharmacy:
                    print(f"Warning: Pharmacy '{ph['pharmacyName']}' not found. Skipping purchase record.")
                    continue
                
                purchase = PurchaseHistory(
                    user_id=user.id,
                    pharmacy_id=pharmacy.id,
                    mask_name=ph['maskName'],  # 用字串存
                    transaction_amount=ph['transactionAmount'],
                    transaction_quantity=ph['transactionQuantity'],
                    transaction_datetime=datetime.strptime(ph['transactionDatetime'], '%Y-%m-%d %H:%M:%S')
                )
                db.session.add(purchase)

        db.session.commit()
        print(f"Loaded {len(data)} users and their purchase histories.")

if __name__ == "__main__":
    load_users('data/users.json')