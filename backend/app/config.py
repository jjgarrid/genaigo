from tinydb import TinyDB
import os

def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'db.json')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return TinyDB(db_path)

db = get_db()
