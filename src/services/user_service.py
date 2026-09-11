from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError


class UserService:

    def __init__(self, mongo):
        self.mongo = mongo

    def get_users(
        self,
        search="",
        department="",
        role=""
    ):
        query = {}

        if search:
            query["$or"] = [
                {
                    "firstName": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "lastName": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "email": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]

        if department:
            query["department"] = department

        if role:
            query["role"] = role

        users = list(
            self.mongo.users.find(query).sort(
                [
                    ("lastName", 1),
                    ("firstName", 1)
                ]
            )
        )

        for user in users:
            user["registrationCount"] = self.get_registration_count(
                user["_id"]
            )

        return users

    def get_registration_count(self, user_id):
        result = self.mongo.events.aggregate([
            {
                "$unwind": "$registrations"
            },
            {
                "$match": {
                    "registrations.userId": user_id
                }
            },
            {
                "$count": "count"
            }
        ])

        result = list(result)

        if result:
            return result[0]["count"]

        return 0

    def get_departments(self):
        return sorted(
            self.mongo.users.distinct("department")
        )

    def get_roles(self):
        return sorted(
            self.mongo.users.distinct("role")
        )

    def get_user_by_id(self, user_id):
        return self.mongo.users.find_one(
            {"_id": user_id}
        )

    def get_user_details(self, user_id):
        user = self.get_user_by_id(user_id)

        if not user:
            return None

        registrations = list(
            self.mongo.events.aggregate([
                {
                    "$unwind": "$registrations"
                },
                {
                    "$match": {
                        "registrations.userId": user_id
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "title": 1,
                        "category": 1,
                        "startDate": 1,
                        "endDate": 1,
                        "location": 1,
                        "registrationStatus":
                            "$registrations.status",
                        "registeredAt":
                            "$registrations.registeredAt"
                    }
                },
                {
                    "$sort": {
                        "startDate": 1
                    }
                }
            ])
        )

        now = datetime.now(timezone.utc)

        upcoming_count = sum(
            1
            for event in registrations
            if event.get("startDate") and
            event["startDate"] >= now
        )

        past_count = sum(
            1
            for event in registrations
            if event.get("startDate") and
            event["startDate"] < now
        )

        user["registrations"] = registrations
        user["upcomingCount"] = upcoming_count
        user["pastCount"] = past_count

        return user

    def create_user(
        self,
        first_name,
        last_name,
        email,
        department,
        role,
        interests
    ):
        user = {
            "firstName": first_name.strip(),
            "lastName": last_name.strip(),
            "email": email.strip().lower(),
            "department": department.strip(),
            "role": role.strip(),
            "interests": interests,
            "createdAt": datetime.now(timezone.utc)
        }

        try:
            return self.mongo.users.insert_one(user)
        except DuplicateKeyError:
            return None

    def update_user(
        self,
        user_id,
        first_name,
        last_name,
        email,
        department,
        role,
        interests
    ):
        update_data = {
            "firstName": first_name.strip(),
            "lastName": last_name.strip(),
            "email": email.strip().lower(),
            "department": department.strip(),
            "role": role.strip(),
            "interests": interests
        }

        try:
            return self.mongo.users.update_one(
                {"_id": user_id},
                {"$set": update_data}
            )
        except DuplicateKeyError:
            return None

    def delete_user(self, user_id):
        referenced = self.mongo.events.find_one(
            {
                "registrations.userId": user_id
            }
        )

        if referenced:
            return {
                "success": False,
                "message": (
                    "Cannot delete this user because "
                    "they are referenced by event registrations."
                )
            }

        result = self.mongo.users.delete_one(
            {"_id": user_id}
        )

        if result.deleted_count == 0:
            return {
                "success": False,
                "message": "User not found."
            }

        return {
            "success": True,
            "message": "User deleted successfully."
        }