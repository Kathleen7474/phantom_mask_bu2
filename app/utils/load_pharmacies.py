import json
import re
from datetime import datetime, time
from app.models import db, Pharmacy, OpeningHour, Mask
from app import create_app

# 將 openingHours 字串解析成多筆 (day_of_week, open_time, close_time)
def parse_opening_hours(opening_hours_str):
    parts = opening_hours_str.split(',')
    result = []
    day_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    for part in parts:
        part = part.strip()
        m = re.match(r'(\w+)\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})', part)
        if m:
            day = m.group(1)
            open_time = datetime.strptime(m.group(2), '%H:%M').time()
            close_raw = m.group(3)
            close_time = time(23, 59) if close_raw == '24:00' else datetime.strptime(close_raw, '%H:%M').time()

            if close_time <= open_time:
                # 跨日營業，拆兩筆
                result.append((day, open_time, time(23, 59)))
                next_day = day_order[(day_order.index(day) + 1) % 7]
                result.append((next_day, time(0, 0), close_time))
            else:
                result.append((day, open_time, close_time))

    return result

def load_pharmacies(json_path):
    app = create_app()
    with app.app_context():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for p in data:
            # 建立 Pharmacy
            pharmacy = Pharmacy(
                name=p['name'],
                cash_balance=p['cashBalance']
            )
            db.session.add(pharmacy)
            # 讓 pharmacy.id 有值，可用於 FK
            # 就是暫時寫入資料庫，但沒有真的提交commit，commit在後面需要FK的時候就會用
            db.session.flush() 

            # 解析並加入 opening hours
            opening_hours = parse_opening_hours(p['openingHours'])
            for day, open_t, close_t in opening_hours:
                oh = OpeningHour(
                    pharmacy_id=pharmacy.id,
                    day_of_week=day,
                    open_time=open_t,
                    close_time=close_t
                )
                db.session.add(oh)
            
            # 加入masks
            for m in p['masks']:
                mask = Mask(
                    pharmacy_id=pharmacy.id,
                    name=m['name'],
                    price=m['price'],
                    stock_quantity=m['stockQuantity']
                )
                db.session.add(mask)

        db.session.commit()
        print(f"Loaded {len(data)} pharmacies into the database.")