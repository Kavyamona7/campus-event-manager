from datetime import datetime, timezone


class DashboardService:
    """MongoDB queries used by the dashboard."""

    def __init__(self, mongo_service):
        self.mongo = mongo_service

    def get_user_count(self):
        """Return the total number of users."""
        return self.mongo.users.count_documents({})

    def get_event_count(self):
        """Return the total number of events."""
        return self.mongo.events.count_documents({})

    def get_upcoming_event_count(self):
        """Return the number of events starting in the future."""
        now = datetime.now(timezone.utc)

        return self.mongo.events.count_documents({
            "startDate": {"$gt": now}
        })

    def get_total_registrations(self):
        """Return the total number of embedded registrations."""
        result = list(
            self.mongo.events.aggregate([
                {
                    "$project": {
                        "registrationCount": {
                            "$size": "$registrations"
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "totalRegistrations": {
                            "$sum": "$registrationCount"
                        }
                    }
                }
            ])
        )

        if not result:
            return 0

        return result[0]["totalRegistrations"]

    def get_upcoming_events(self, limit=5):
        """Return the next upcoming events."""
        now = datetime.now(timezone.utc)

        events = list(
            self.mongo.events.find(
                {"startDate": {"$gt": now}},
                {
                    "title": 1,
                    "category": 1,
                    "startDate": 1,
                    "location": 1,
                    "capacity": 1,
                    "registrations": 1
                }
            ).sort("startDate", 1).limit(limit)
        )

        for event in events:
            event["confirmedCount"] = sum(
                1
                for registration in event.get("registrations", [])
                if registration.get("status") == "confirmed"
            )

        return events

    def get_most_popular_event(self):
        """Return the event with the highest confirmed registration count."""

        result = list(
            self.mongo.events.aggregate([
                {
                    "$project": {
                        "title": 1,
                        "category": 1,
                        "startDate": 1,
                        "capacity": 1,
                        "confirmedCount": {
                            "$size": {
                                "$filter": {
                                    "input": "$registrations",
                                    "as": "registration",
                                    "cond": {
                                        "$eq": [
                                            "$$registration.status",
                                            "confirmed"
                                        ]
                                    }
                                }
                            }
                        }
                    }
                },
                {
                    "$sort": {
                        "confirmedCount": -1,
                        "startDate": 1
                    }
                },
                {
                    "$limit": 1
                }
            ])
        )

        return result[0] if result else None

    def get_dashboard_data(self):
        """Return all data required by the dashboard."""

        return {
            "user_count": self.get_user_count(),
            "event_count": self.get_event_count(),
            "upcoming_event_count": self.get_upcoming_event_count(),
            "total_registrations": self.get_total_registrations(),
            "upcoming_events": self.get_upcoming_events(5),
            "most_popular_event": self.get_most_popular_event()
        }