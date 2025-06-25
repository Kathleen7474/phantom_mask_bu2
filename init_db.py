# init_db.py
from create_db import create_database
from app.utils.load_pharmacies import load_pharmacies
from app.utils.load_users import load_users
from app.models import Pharmacy

def initialize():
    create_database()
    load_pharmacies('data/pharmacies.json')
    load_users('data/users.json')

    print("Initialization complete.")


if __name__ == "__main__":
    initialize()