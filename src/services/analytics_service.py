from datetime import datetime, timezone


class AnalyticsService:

    def __init__(self, mongo):
        self.mongo = mongo

    # A. Registrations by category
    def registrations_by_category(self):
        return list(
            self.mongo.events.aggregate([
                {
                    "$project": {
                        "category": 1,
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
                    "$group": {
                        "_id": "$category",
                        "numberOfEvents": {
                            "$sum": 1
                        },
                        "totalConfirmed": {
                            "$sum": "$confirmedCount"
                        }
                    }
                },
                {
                    "$sort": {
                        "totalConfirmed": -1
                    }
                }
            ])
        )

    # B. Top 5 events
    def top_events(self):
        return list(
            self.mongo.events.aggregate([
                {
                    "$project": {
                        "title": 1,
                        "category": 1,
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
                    "$addFields": {
                        "occupancy": {
                            "$multiply": [
                                {
                                    "$divide": [
                                        "$confirmedCount",
                                        "$capacity"
                                    ]
                                },
                                100
                            ]
                        }
                    }
                },
                {
                    "$sort": {
                        "confirmedCount": -1
                    }
                },
                {
                    "$limit": 5
                }
            ])
        )

    # C. Users with no registration
    def users_with_no_registration(self):
        return list(
            self.mongo.users.aggregate([
                {
                    "$lookup": {
                        "from": "events",
                        "let": {
                            "user_id": "$_id"
                        },
                        "pipeline": [
                            {
                                "$unwind": "$registrations"
                            },
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": [
                                            "$registrations.userId",
                                            "$$user_id"
                                        ]
                                    }
                                }
                            }
                        ],
                        "as": "registeredEvents"
                    }
                },
                {
                    "$match": {
                        "$expr": {
                            "$eq": [
                                {
                                    "$size": "$registeredEvents"
                                },
                                0
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "firstName": 1,
                        "lastName": 1,
                        "email": 1,
                        "department": 1,
                        "role": 1
                    }
                },
                {
                    "$sort": {
                        "lastName": 1,
                        "firstName": 1
                    }
                }
            ])
        )

    # D. Events above average occupancy
    def events_above_average_occupancy(self):
        pipeline = [
            {
                "$project": {
                    "title": 1,
                    "category": 1,
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
                "$addFields": {
                    "occupancy": {
                        "$multiply": [
                            {
                                "$divide": [
                                    "$confirmedCount",
                                    "$capacity"
                                ]
                            },
                            100
                        ]
                    }
                }
            }
        ]

        average_result = list(
            self.mongo.events.aggregate(
                pipeline + [
                    {
                        "$group": {
                            "_id": None,
                            "averageOccupancy": {
                                "$avg": "$occupancy"
                            }
                        }
                    }
                ]
            )
        )

        average_occupancy = (
            average_result[0]["averageOccupancy"]
            if average_result
            else 0
        )

        results = list(
            self.mongo.events.aggregate(
                pipeline + [
                    {
                        "$match": {
                            "$expr": {
                                "$gt": [
                                    "$occupancy",
                                    average_occupancy
                                ]
                            }
                        }
                    },
                    {
                        "$sort": {
                            "occupancy": -1
                        }
                    }
                ]
            )
        )

        return {
            "averageOccupancy": average_occupancy,
            "events": results
        }

    # E. Most used tags
    def most_used_tags(self):
        return list(
            self.mongo.events.aggregate([
                {
                    "$unwind": "$tags"
                },
                {
                    "$group": {
                        "_id": "$tags",
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$sort": {
                        "count": -1,
                        "_id": 1
                    }
                }
            ])
        )

    # F. Events by month
    def events_by_month(self):
        return list(
            self.mongo.events.aggregate([
                {
                    "$unwind": {
                        "path": "$registrations",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "year": {
                                "$year": "$startDate"
                            },
                            "month": {
                                "$month": "$startDate"
                            }
                        },
                        "numberOfEvents": {
                            "$addToSet": "$_id"
                        },
                        "registrations": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$eq": [
                                            "$registrations.status",
                                            "confirmed"
                                        ]
                                    },
                                    1,
                                    0
                                ]
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "year": "$_id.year",
                        "month": "$_id.month",
                        "numberOfEvents": {
                            "$size": "$numberOfEvents"
                        },
                        "registrations": 1
                    }
                },
                {
                    "$sort": {
                        "year": 1,
                        "month": 1
                    }
                }
            ])
        )

    def get_all_analytics(self):
        return {
            "by_category": self.registrations_by_category(),
            "top_events": self.top_events(),
            "no_registration": self.users_with_no_registration(),
            "above_average": self.events_above_average_occupancy(),
            "tags": self.most_used_tags(),
            "by_month": self.events_by_month()
        }