// Campus Event Manager
// MongoDB database initialization script

// Switch to the required database
const dbName = "campus_events";
const campusDB = db.getSiblingDB(dbName);

// WARNING: This resets the local project database.
// It is safe during development before final submission.
campusDB.dropDatabase();

print("Creating database: " + dbName);

// ============================================================
// USERS COLLECTION
// ============================================================

campusDB.createCollection("users", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: [
                "firstName",
                "lastName",
                "email",
                "department",
                "role",
                "interests",
                "createdAt"
            ],
            properties: {
                firstName: {
                    bsonType: "string",
                    minLength: 1
                },
                lastName: {
                    bsonType: "string",
                    minLength: 1
                },
                email: {
                    bsonType: "string",
                    minLength: 5,
                    pattern: "^.+@.+\\..+$"
                },
                department: {
                    bsonType: "string",
                    minLength: 1
                },
                role: {
                    bsonType: "string",
                    enum: [
                        "student",
                        "faculty",
                        "staff",
                        "admin"
                    ]
                },
                interests: {
                    bsonType: "array",
                    items: {
                        bsonType: "string"
                    }
                },
                createdAt: {
                    bsonType: "date"
                }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
});

// Unique email index
campusDB.users.createIndex(
    { email: 1 },
    { unique: true, name: "idx_users_email_unique" }
);

print("Users collection created.");
print("Unique email index created.");

// ============================================================
// EVENTS COLLECTION
// ============================================================

campusDB.createCollection("events", {
    validator: {
        $and: [
            {
                $jsonSchema: {
                    bsonType: "object",
                    required: [
                        "title",
                        "description",
                        "category",
                        "tags",
                        "startDate",
                        "endDate",
                        "capacity",
                        "location",
                        "organizerId",
                        "registrations",
                        "createdAt"
                    ],
                    properties: {

                        title: {
                            bsonType: "string",
                            minLength: 1
                        },

                        description: {
                            bsonType: "string"
                        },

                        category: {
                            bsonType: "string",
                            minLength: 1
                        },

                        tags: {
                            bsonType: "array",
                            items: {
                                bsonType: "string"
                            }
                        },

                        startDate: {
                            bsonType: "date"
                        },

                        endDate: {
                            bsonType: "date"
                        },

                        capacity: {
                            bsonType: "int",
                            minimum: 1
                        },

                        location: {
                            bsonType: "object",
                            required: [
                                "building",
                                "room",
                                "campus"
                            ],
                            properties: {

                                building: {
                                    bsonType: "string",
                                    minLength: 1
                                },

                                room: {
                                    bsonType: "string",
                                    minLength: 1
                                },

                                campus: {
                                    bsonType: "string",
                                    minLength: 1
                                }
                            }
                        },

                        organizerId: {
                            bsonType: "objectId"
                        },

                        registrations: {
                            bsonType: "array",
                            items: {
                                bsonType: "object",
                                required: [
                                    "userId",
                                    "registeredAt",
                                    "status"
                                ],
                                properties: {

                                    userId: {
                                        bsonType: "objectId"
                                    },

                                    registeredAt: {
                                        bsonType: "date"
                                    },

                                    status: {
                                        bsonType: "string",
                                        enum: [
                                            "confirmed",
                                            "cancelled",
                                            "waiting"
                                        ]
                                    }
                                }
                            }
                        },

                        createdAt: {
                            bsonType: "date"
                        }
                    }
                }
            },

            // End date cannot be before start date
            {
                $expr: {
                    $lte: [
                        "$startDate",
                        "$endDate"
                    ]
                }
            }
        ]
    },

    validationLevel: "strict",
    validationAction: "error"
});

// Required event indexes
campusDB.events.createIndex(
    { startDate: 1 },
    { name: "idx_events_startDate" }
);

campusDB.events.createIndex(
    { category: 1 },
    { name: "idx_events_category" }
);

print("Events collection created.");
print("Event indexes created.");

// ============================================================
// FINAL INFORMATION
// ============================================================

print("");
print("==============================================");
print("Campus Event Manager database initialized!");
print("Database: " + dbName);
print("Collections:");
print(" - users");
print(" - events");
print("Indexes:");
print(" - users.email (unique)");
print(" - events.startDate");
print(" - events.category");
print("==============================================");