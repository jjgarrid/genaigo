import os
import sys
from tinydb import TinyDB

# Add backend to Python path for imports
backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, backend_dir)

from app.services.gmail_fetcher import GmailFetcher
import app.config


def test_fetcher_uses_main_db(monkeypatch, tmp_path):
    temp_db_path = tmp_path / "db.json"

    def mock_get_db():
        return TinyDB(temp_db_path)

    monkeypatch.setattr(app.config, "get_db", mock_get_db)
    fetcher = GmailFetcher()
    table = fetcher._get_messages_db()
    assert table._storage._handle.name == str(temp_db_path)

    sample = {
        "messageId": "id123",
        "subject": "Hi",
        "sender": "a@b.com",
        "date": "today",
        "retrievalTimestamp": "ts",
        "body": "body",
        "bodyHash": "hash",
    }
    table.insert(sample)
    retrieved = fetcher.get_stored_messages(limit=1)
    assert retrieved[0]["messageId"] == "id123"
