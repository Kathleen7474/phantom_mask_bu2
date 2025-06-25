# app/routes/pharmacy.py

from flask import Blueprint, jsonify, abort
from app.models import db,Pharmacy, Mask
from flask import request
from datetime import datetime
from app.utils.search_utils import compute_score


# blueprint的用途是幫API組成群組
# 如果有很多支API就不會讓一堆API都塞在同一個檔案
pharmacy_bp = Blueprint('pharmacy', __name__)



# http://127.0.0.1:5000/pharmacies?day=Mon&time=15:30
# http://127.0.0.1:5000/pharmacies  -->return all
@pharmacy_bp.route('/pharmacies', methods=['GET','POST'])
def get_pharmacies_by_time():
    allowed_days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    day = request.args.get('day')  # 可能是 'Mon'
    time_str = request.args.get('time')  # 可能是 '15:30'
    
    query_time = None
    if day and day not in allowed_days:
        return jsonify({"error": f"Invalid day parameter. Allowed values: {allowed_days}"}), 400
    if time_str:
        try:
            query_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            return jsonify({"error": "Invalid time format, expected HH:MM"}), 400

    pharmacies = []
    all_pharmacies = Pharmacy.query.all()

    for p in all_pharmacies:
        for h in p.opening_hours:
            # 條件：符合 day（如果有給）+ 符合 time（如果有給）
            day_ok = (not day) or (h.day_of_week == day)
            time_ok = (not query_time) or (h.open_time <= query_time <= h.close_time)

            if day_ok and time_ok:
                pharmacies.append(p)
                break  # 一個符合就加入，不檢查其他時段

    # 如果 day 和 time 都沒提供，就顯示所有藥局
    if not day and not time_str:
        pharmacies = all_pharmacies

    result = []
    for p in pharmacies:
        hours = [
            {
                "day": h.day_of_week,
                "open": h.open_time.strftime('%H:%M'),
                "close": h.close_time.strftime('%H:%M')
            }
            for h in p.opening_hours
        ]
        result.append({
            "id": p.id,
            "name": p.name,
            "openingHours": hours
        })

    return jsonify(result)


# http://127.0.0.1:5000/pharmacies/1/masks
# http://127.0.0.1:5000/pharmacies/3/masks?sort_by=name
# http://127.0.0.1:5000/pharmacies/3/masks?sort_by=price
@pharmacy_bp.route('/pharmacies/<int:pharmacy_id>/masks', methods=['GET', 'POST'])
def list_masks_of_pharmacy(pharmacy_id):
    sort_by = request.args.get('sort_by', None)

    # pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    pharmacy = db.session.get(Pharmacy, pharmacy_id)
    if not pharmacy:
        abort(404)
    masks = pharmacy.masks
    
    if sort_by == 'name':
        masks = sorted(masks, key=lambda m: m.name.lower())
    elif sort_by == 'price':
        masks = sorted(masks, key=lambda m: m.price)

    result = [
        {
            "id": m.id,
            "name": m.name,
            "price": m.price,
            "stockQuantity": m.stock_quantity
        }
        for m in masks
    ]
    return jsonify({
        "pharmacy": pharmacy.name,
        "masks": result
    })


@pharmacy_bp.route('/pharmacies/mask_count_by_price', methods=['GET'])
def mask_count_by_price():
    try:
        lower_price = float(request.args.get('lower_price', 0))
        upper_price = float(request.args.get('upper_price', float('inf')))
        threshold_lower = int(request.args.get('threshold_lower', 0))
        threshold_upper_str = request.args.get('threshold_upper')
        if threshold_upper_str is not None:
            threshold_upper = int(threshold_upper_str)
        else:
            threshold_upper = float('inf')
    except ValueError:
        return jsonify({"error": "Invalid query parameters"}), 400
    
    if upper_price < lower_price:
        return jsonify({"error": "upper_price must be greater than or equal to lower_price"}), 400
    if isinstance(threshold_upper, (int, float)) and threshold_upper < threshold_lower:
        return jsonify({"error": "threshold_upper must be greater than or equal to threshold_lower"}), 400

    pharmacies = Pharmacy.query.all()
    result = {"below": [], "between": [], "above": []}

    for p in pharmacies:
        matching_masks = [m for m in p.masks if lower_price <= m.price <= upper_price]
        count = len(matching_masks)

        pharmacy_info = {
            "id": p.id,
            "name": p.name,
            "matchingMaskCount": count,
            "matchingMasks": [
                {
                    "id": m.id,
                    "name": m.name,
                    "price": m.price
                } for m in matching_masks
            ]
        }

        if count < threshold_lower:
            result["below"].append(pharmacy_info)
        elif threshold_lower <= count <= threshold_upper:
            result["between"].append(pharmacy_info)
        else:
            result["above"].append(pharmacy_info)

    return jsonify(result)

# 調整qunatity用
@pharmacy_bp.route('/pharmacies/<int:pharmacy_id>/masks/adjust', methods=['POST'])
def adjust_mask_quantity(pharmacy_id):
    data = request.get_json()
    
    if not data or 'mask_name' not in data or 'adjustment' not in data:
        return jsonify({"error": "Missing 'mask_name' or 'adjustment' in request body"}), 400

    mask_name = data['mask_name'].strip()
    adjustment = data['adjustment']

    # 驗證 adjustment 是數字
    if not isinstance(adjustment, (int, float)):
        return jsonify({"error": "'adjustment' must be a number"}), 400

    # 查找對應的 mask
    mask = Mask.query.filter_by(pharmacy_id=pharmacy_id, name=mask_name).first()
    if not mask:
        return jsonify({"error": f"Mask '{mask_name}' not found in pharmacy id {pharmacy_id}"}), 404

    # 計算新的庫存
    new_quantity = mask.stock_quantity + adjustment
    if new_quantity < 0:
        return jsonify({"error": "Stock quantity cannot be negative"}), 400

    # 更新並儲存
    mask.stock_quantity = new_quantity
    db.session.commit()

    return jsonify({
        "message": "Stock updated successfully",
        "mask_name": mask.name,
        "new_stock_quantity": new_quantity
    }), 200

# 整批調整
# ps. 如果是新建mask的話，他的編號會在超級後面
@pharmacy_bp.route('/pharmacies/<int:pharmacy_id>/masks/batch', methods=['POST'])
def create_or_update_masks(pharmacy_id):
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    data = request.get_json()

    if not data or 'masks' not in data:
        return jsonify({"error": "Missing 'masks' data"}), 400

    results = []

    for item in data['masks']:
        name = item.get('name', '').strip()
        price = item.get('price')
        stock_quantity = item.get('stock_quantity')

        # if not name or price is None or stock_quantity is None:
        #     results.append({"mask": name or "(missing name)", "status": "invalid input"})
        #     continue
        
        if not name:
            results.append({"mask": "(missing name)", "status": "invalid input"})
            continue

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
        except (ValueError, TypeError):
            results.append({"mask": name, "status": "invalid input"})
            continue

        # 檢查是否已存在
        mask = next((m for m in pharmacy.masks if m.name == name), None)

        if mask:
            mask.price = price
            mask.stock_quantity = stock_quantity
            status = 'updated'
        else:
            new_mask = Mask(
                pharmacy_id=pharmacy.id,
                name=name,
                price=price,
                stock_quantity=stock_quantity
            )
            db.session.add(new_mask)
            status = 'created'

        results.append({"mask": name, "status": status})

    db.session.commit()
    return jsonify({"results": results})



@pharmacy_bp.route('/search', methods=['GET'])
def search_pharmacy_or_mask():
    query = request.args.get('q', '').strip()
    limit = request.args.get('limit', 10)

    if not query:
        return jsonify({"error": "Search query is required"}), 400

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({"error": "Limit must be an integer"}), 400

    keywords = query.split()
    results = []

    pharmacies = Pharmacy.query.all()

    for p in pharmacies:
        for m in p.masks:
            score = compute_score(p.name, m.name, keywords)
            # print("pharmacy", p.name, " mask ", m.name)
            if score > 0:
                results.append({
                    "pharmacy": p.name,
                    "mask": m.name,
                    "price": m.price,
                    "stock": m.stock_quantity,
                    "score": score
                })

    # 按照分數排序後，截斷為最多 limit 筆
    results = sorted(results, key=lambda x: x['score'], reverse=True)[:limit]

    return jsonify(results)