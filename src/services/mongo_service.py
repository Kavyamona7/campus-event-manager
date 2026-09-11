from pymongo import MongoClient

from config import MONGO_URI, MONGO_DB_NAME


class MongoService:
    """Central MongoDB connection service."""

    def __init__(self):
        self.client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
        self.db = self.client[MONGO_DB_NAME]

    def ping(self):
        """Check that MongoDB is reachable."""
        self.client.admin.command("ping")
        return True

    @property
    def users(self):
        """Return the users collection."""
        return self.db["users"]

    @property
    def events(self):
        """Return the events collection."""
        return self.db["events"]

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()