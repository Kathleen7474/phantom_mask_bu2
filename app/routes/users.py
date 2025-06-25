# users.py

from flask import Blueprint, jsonify
from app.models import db, User, PurchaseHistory, Mask, Pharmacy
from flask import request
from datetime import datetime

user_bp = Blueprint('user', __name__)


# http://127.0.0.1:5000/users/top-spenders?start=2024-01-01&end=2025-01-31&n=5
# 有空再來寫直接用資料庫篩選
# 還有如果沒給時間就直接all time
@user_bp.route('/users/top-spenders', methods=['GET', 'POST'])
def top_spenders():
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    # top_n = int(request.args.get('n', 5))   
    n_str = request.args.get('n', '5')# 預設取前 5 名

    try:
        top_n = int(n_str)
    except ValueError:
        return jsonify({"error": "Invalid 'n' parameter. Must be an integer."}), 400

    # 如果有給 start 或 end，才做日期轉換
    try:
        start_date = datetime.strptime(start_str, '%Y-%m-%d') if start_str else None
        end_date = datetime.strptime(end_str, '%Y-%m-%d') if end_str else None
    except:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    users = User.query.all()
    user_spending = []

    for u in users:
        total = 0
        for ph in u.purchase_histories:
            # 如果指定了時間，就比對範圍
            if (not start_date or ph.transaction_datetime >= start_date) and \
               (not end_date or ph.transaction_datetime <= end_date):
                total += ph.transaction_amount * ph.transaction_quantity
        user_spending.append((u.id, u.name, total))

    # 排序 & 取前 N 名
    # top_users = sorted(user_spending, key=lambda x: x[1], reverse=True)[:top_n]
    top_users = sorted(user_spending, key=lambda x: x[2], reverse=True)[:top_n]

    return jsonify([
        {
            "id": user_id,
            "name": name,
            "total_spending": round(amount, 2)
        }
        for user_id, name, amount in top_users
    ])




@user_bp.route('/users/<int:user_id>/purchase', methods=['POST'])
def process_purchase(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data or 'items' not in data:
        return jsonify({"error": "Missing purchase items"}), 400

    total_cost = 0
    purchase_records = []
    now = datetime.now()
    current_day = now.strftime('%a')  # e.g., "Mon"
    if current_day == "Thu":
        current_day = "Thur"
    current_time = now.time()

    for item in data['items']:
        pharmacy_id = item.get('pharmacy_id')
        if not pharmacy_id:
            return jsonify({"error": "Missing pharmacy_id in an item"}), 400

        pharmacy = Pharmacy.query.get(pharmacy_id)
        if not pharmacy:
            return jsonify({"error": f"Pharmacy with id '{pharmacy_id}' not found"}), 404

        # ➕ 檢查營業時間
        open_now = False
        for h in pharmacy.opening_hours:
            if h.day_of_week == current_day and h.open_time <= current_time <= h.close_time:
                open_now = True
                break

        if not open_now:
            return jsonify({
                "error": f"Pharmacy '{pharmacy.name}' is currently closed (now: {current_day} {current_time.strftime('%H:%M')})"
            }), 400

        mask_name = item.get('mask_name', '').strip()
        if not mask_name:
            return jsonify({"error": "Missing mask_name in an item"}), 400

        mask = Mask.query.filter_by(pharmacy_id=pharmacy_id, name=mask_name).first()
        if not mask:
            return jsonify({"error": f"Mask '{mask_name}' not found in pharmacy id '{pharmacy_id}'"}), 404

        quantity = item.get('quantity', 0)
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": f"Invalid quantity for '{mask_name}'"}), 400

        if mask.stock_quantity < quantity:
            return jsonify({"error": f"Not enough stock for '{mask_name}' in pharmacy id '{pharmacy_id}'"}), 400

        cost = mask.price * quantity
        total_cost += cost

        purchase = PurchaseHistory(
            user_id=user.id,
            pharmacy_id=pharmacy_id,
            mask_name=mask.name,
            transaction_amount=mask.price,
            transaction_quantity=quantity,
            transaction_datetime=now
        )
        purchase_records.append(purchase)

        # 更新庫存與藥局現金
        mask.stock_quantity -= quantity
        pharmacy.cash_balance += cost

    if user.cash_balance < total_cost:
        return jsonify({"error": "User does not have enough balance"}), 400

    user.cash_balance -= total_cost

    for record in purchase_records:
        db.session.add(record)
    db.session.commit()

    return jsonify({
        "message": "Purchase completed successfully",
        "total_spent": round(total_cost, 2),
        "remaining_balance": round(user.cash_balance, 2)
    })