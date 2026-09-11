import re
from datetime import datetime, timezone


class EventService:
    """MongoDB operations for campus events."""

    def __init__(self, mongo_service):
        self.mongo = mongo_service

    def get_events(
        self,
        title=None,
        category=None,
        status=None,
        tag=None,
        sort_order="asc"
    ):
        """
        Return events with optional filters.

        Supported filters:
        - title: partial title search
        - category: exact category
        - status: upcoming or past
        - tag: exact tag
        - sort_order: asc or desc
        """

        pipeline = []

        # ----------------------------------------------------
        # Calculate confirmed registrations
        # ----------------------------------------------------

        pipeline.append({
            "$addFields": {
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
        })

        # ----------------------------------------------------
        # Calculate occupancy percentage
        # ----------------------------------------------------

        pipeline.append({
            "$addFields": {
                "occupancy": {
                    "$cond": [
                        {"$gt": ["$capacity", 0]},
                        {
                            "$multiply": [
                                {
                                    "$divide": [
                                        "$confirmedCount",
                                        "$capacity"
                                    ]
                                },
                                100
                            ]
                        },
                        0
                    ]
                }
            }
        })

        # ----------------------------------------------------
        # Filters
        # ----------------------------------------------------

        filters = {}

        # Title search
        if title and title.strip():
            filters["title"] = {
                "$regex": re.escape(title.strip()),
                "$options": "i"
            }

        # Category filter
        if category and category.strip():
            filters["category"] = category.strip()

        # Tag filter
        if tag and tag.strip():
            filters["tags"] = tag.strip()

        # Upcoming / past filter
        if status in ("upcoming", "past"):
            now = datetime.now(timezone.utc)

            if status == "upcoming":
                filters["startDate"] = {
                    "$gt": now
                }
            else:
                filters["startDate"] = {
                    "$lte": now
                }

        if filters:
            pipeline.append({
                "$match": filters
            })

        # ----------------------------------------------------
        # Sort by start date
        # ----------------------------------------------------

        sort_direction = 1 if sort_order == "asc" else -1

        pipeline.append({
            "$sort": {
                "startDate": sort_direction
            }
        })

        # ----------------------------------------------------
        # Execute query
        # ----------------------------------------------------

        return list(
            self.mongo.events.aggregate(pipeline)
        )

    def get_event_by_id(self, event_id):
        """Return a single event by MongoDB ObjectId."""

        return self.mongo.events.find_one({
            "_id": event_id
        })

    def get_categories(self):
        """Return all event categories."""

        return sorted(
            self.mongo.events.distinct("category")
        )

    def get_tags(self):
        """Return all unique event tags."""

        result = self.mongo.events.aggregate([
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags"}},
            {"$sort": {"_id": 1}}
        ])

        return [
            document["_id"]
            for document in result
        ]

    def get_event_count(self):
        """Return total number of events."""

        return self.mongo.events.count_documents({})

    def create_event(
        self,
        title,
        description,
        category,
        tags,
        start_date,
        end_date,
        capacity,
        building,
        room,
        campus,
        organizer_id
    ):
        """Create a new campus event."""

        event = {
            "title": title.strip(),
            "description": description.strip(),
            "category": category.strip(),
            "tags": [
                tag.strip()
                for tag in tags
                if tag.strip()
            ],
            "startDate": start_date,
            "endDate": end_date,
            "capacity": capacity,
            "location": {
                "building": building.strip(),
                "room": room.strip(),
                "campus": campus.strip()
            },
            "organizerId": organizer_id,
            "registrations": [],
            "createdAt": datetime.now(timezone.utc)
        }

        result = self.mongo.events.insert_one(event)

        return result.inserted_id

    def get_organizers(self):
        """Return users who can organize events."""

        return list(
            self.mongo.users.find(
                {},
                {
                    "firstName": 1,
                    "lastName": 1,
                    "email": 1
                }
            ).sort([
                ("lastName", 1),
                ("firstName", 1)
            ])
        )

    def update_event(
        self,
        event_id,
        title,
        description,
        category,
        tags,
        start_date,
        end_date,
        capacity,
        building,
        room,
        campus,
        organizer_id
    ):
    

        update_data = {
            "title": title.strip(),
            "description": description.strip(),
            "category": category.strip(),
            "tags": [tag.strip() for tag in tags if tag.strip()],
            "startDate": start_date,
            "endDate": end_date,
            "capacity": capacity,
            "location": {
                "building": building.strip(),
                "room": room.strip(),
                "campus": campus.strip()
            },
            "organizerId": organizer_id
        }

        result = self.mongo.events.update_one(
            {"_id": event_id},
            {"$set": update_data}
        )

        return result

    def get_event_details(self, event_id):
        """Return event details together with organizer information."""

        event = self.mongo.events.find_one({"_id": event_id})

        if not event:
            return None

        organizer = self.mongo.users.find_one(
            {"_id": event.get("organizerId")},
            {
                "firstName": 1,
                "lastName": 1,
                "email": 1,
                "department": 1,
                "role": 1
            }
        )

        confirmed_count = sum(
            1
            for registration in event.get("registrations", [])
            if registration.get("status") == "confirmed"
        )

        event["confirmedCount"] = confirmed_count

        if event.get("capacity", 0) > 0:
            event["occupancy"] = (
                confirmed_count / event["capacity"]
            ) * 100
        else:
            event["occupancy"] = 0

        event["organizer"] = organizer

        return event

    def get_registration_users(self):
        """Return all users available for event registration."""

        return list(
            self.mongo.users.find(
                {},
                {
                    "firstName": 1,
                    "lastName": 1,
                    "email": 1
                }
            ).sort([
                ("lastName", 1),
                ("firstName", 1)
            ])
        )

    def get_registered_users(self, registrations):
        """Return user information for the event registrations."""

        user_ids = [
            registration["userId"]
            for registration in registrations
            if registration.get("userId")
        ]

        if not user_ids:
            return []

        users = self.mongo.users.find(
            {"_id": {"$in": user_ids}},
            {
                "firstName": 1,
                "lastName": 1,
                "email": 1,
                "department": 1,
                "role": 1
            }
        )

        users_by_id = {
            user["_id"]: user
            for user in users
        }

        result = []

        for registration in registrations:
            user = users_by_id.get(registration.get("userId"))

            if user:
                result.append({
                    "user": user,
                    "status": registration.get("status"),
                    "registeredAt": registration.get("registeredAt")
                })

        return result

    def register_user(self, event_id, user_id):
        """Register a user for an event."""

        event = self.mongo.events.find_one(
            {"_id": event_id}
        )

        if not event:
            return {
                "success": False,
                "message": "Event not found."
            }

        # Prevent duplicate registration
        existing = next(
            (
                registration
                for registration in event.get("registrations", [])
                if registration.get("userId") == user_id
            ),
            None
        )

        if existing:
            return {
                "success": False,
                "message": "User is already registered for this event."
            }

        confirmed_count = sum(
            1
            for registration in event.get("registrations", [])
            if registration.get("status") == "confirmed"
        )

        if confirmed_count >= event.get("capacity", 0):
            return {
                "success": False,
                "message": "This event is full."
            }

        registration = {
            "userId": user_id,
            "registeredAt": datetime.now(timezone.utc),
            "status": "confirmed"
        }

        self.mongo.events.update_one(
            {"_id": event_id},
            {"$push": {"registrations": registration}}
        )

        return {
            "success": True,
            "message": "User registered successfully."
        }

    def cancel_registration(self, event_id, user_id):
        """Remove a user's registration from an event."""

        result = self.mongo.events.update_one(
            {"_id": event_id},
            {
                "$pull": {
                    "registrations": {
                        "userId": user_id
                    }
                }
            }
        )

        if result.matched_count == 0:
            return {
                "success": False,
                "message": "Event not found."
            }

        if result.modified_count == 0:
            return {
                "success": False,
                "message": "Registration not found."
            }

        return {
            "success": True,
            "message": "Registration cancelled."
        }

    def delete_event(self, event_id):
        result = self.mongo.events.delete_one(
            {"_id": event_id}
        )

        return result