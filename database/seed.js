const campusDB = db.getSiblingDB("campus_events");

// Reproducible seed:
// clear existing data but keep the collections, validators and indexes.
campusDB.users.deleteMany({});
campusDB.events.deleteMany({});


// ------------------------------------------------------------
// USERS
// ------------------------------------------------------------

const users = [
  {
    _id: ObjectId("000000000000000000000001"),
    firstName: "Aarav",
    lastName: "Sharma",
    email: "aarav.sharma@campus.fr",
    department: "Data Science",
    role: "student",
    interests: ["Data", "AI", "Cloud"],
    createdAt: ISODate("2026-05-01T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000002"),
    firstName: "Emma",
    lastName: "Martin",
    email: "emma.martin@campus.fr",
    department: "Computer Science",
    role: "student",
    interests: ["AI", "Cybersecurity", "Technology"],
    createdAt: ISODate("2026-05-02T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000003"),
    firstName: "Lucas",
    lastName: "Bernard",
    email: "lucas.bernard@campus.fr",
    department: "Cloud Computing",
    role: "student",
    interests: ["Cloud", "Technology", "Open Source"],
    createdAt: ISODate("2026-05-03T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000004"),
    firstName: "Sofia",
    lastName: "Dubois",
    email: "sofia.dubois@campus.fr",
    department: "Data Engineering",
    role: "student",
    interests: ["Data", "Python", "Analytics"],
    createdAt: ISODate("2026-05-04T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000005"),
    firstName: "Thomas",
    lastName: "Robert",
    email: "thomas.robert@campus.fr",
    department: "Business",
    role: "student",
    interests: ["Entrepreneurship", "Career", "Leadership"],
    createdAt: ISODate("2026-05-05T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000006"),
    firstName: "Chloe",
    lastName: "Petit",
    email: "chloe.petit@campus.fr",
    department: "Cybersecurity",
    role: "student",
    interests: ["Cybersecurity", "Technology", "AI"],
    createdAt: ISODate("2026-05-06T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000007"),
    firstName: "Hugo",
    lastName: "Moreau",
    email: "hugo.moreau@campus.fr",
    department: "Software Engineering",
    role: "student",
    interests: ["Technology", "Hackathon", "Open Source"],
    createdAt: ISODate("2026-05-07T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000008"),
    firstName: "Amelie",
    lastName: "Laurent",
    email: "amelie.laurent@campus.fr",
    department: "Cloud Computing",
    role: "student",
    interests: ["Cloud", "Wellness", "Sports"],
    createdAt: ISODate("2026-05-08T09:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000009"),
    firstName: "Nathan",
    lastName: "Simon",
    email: "nathan.simon@campus.fr",
    department: "Data Engineering",
    role: "student",
    interests: ["Data", "Machine Learning", "Analytics"],
    createdAt: ISODate("2026-05-09T09:00:00Z")
  },
  {
    _id: ObjectId("00000000000000000000000a"),
    firstName: "Lea",
    lastName: "Michel",
    email: "lea.michel@campus.fr",
    department: "Business",
    role: "student",
    interests: ["Career", "Leadership", "Entrepreneurship"],
    createdAt: ISODate("2026-05-10T09:00:00Z")
  },
  {
    _id: ObjectId("00000000000000000000000b"),
    firstName: "Louis",
    lastName: "Garcia",
    email: "louis.garcia@campus.fr",
    department: "Computer Science",
    role: "student",
    interests: ["AI", "Technology", "Research"],
    createdAt: ISODate("2026-05-11T09:00:00Z")
  },
  {
    _id: ObjectId("00000000000000000000000c"),
    firstName: "Camille",
    lastName: "Roux",
    email: "camille.roux@campus.fr",
    department: "Arts",
    role: "student",
    interests: ["Arts", "Culture", "Community"],
    createdAt: ISODate("2026-05-12T09:00:00Z")
  },
  {
    _id: ObjectId("00000000000000000000000d"),
    firstName: "Gabriel",
    lastName: "Fournier",
    email: "gabriel.fournier@campus.fr",
    department: "Research",
    role: "faculty",
    interests: ["Research", "Innovation", "Technology"],
    createdAt: ISODate("2026-05-13T09:00:00Z")
  },
  {
    _id: ObjectId("00000000000000000000000e"),
    firstName: "Alice",
    lastName: "Mercier",
    email: "alice.mercier@campus.fr",
    department: "Data Science",
    role: "faculty",
    interests: ["Data", "AI", "Research"],
    createdAt: ISODate("2026-05-14T09:00:00Z")
  },
  {
    _id: ObjectId("00000000000000000000000f"),
    firstName: "Paul",
    lastName: "Girard",
    email: "paul.girard@campus.fr",
    department: "Administration",
    role: "staff",
    interests: ["Community", "Leadership", "Events"],
    createdAt: ISODate("2026-05-15T09:00:00Z")
  }
];

campusDB.users.insertMany(users);


// ------------------------------------------------------------
// HELPER FOR REGISTRATIONS
// ------------------------------------------------------------

function registration(userId, registeredAt, status = "confirmed") {
  return {
    userId: userId,
    registeredAt: ISODate(registeredAt),
    status: status
  };
}


// ------------------------------------------------------------
// EVENTS
// ------------------------------------------------------------

const events = [
  {
    _id: ObjectId("100000000000000000000001"),
    title: "Data Analytics Workshop",
    description: "Hands-on workshop covering data analysis and practical analytics techniques.",
    category: "Workshop",
    tags: ["Data", "Python", "Analytics"],
    startDate: ISODate("2026-06-15T10:00:00Z"),
    endDate: ISODate("2026-06-15T12:00:00Z"),
    capacity: NumberInt(30),
    location: {
      building: "Innovation Center",
      room: "B204",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000004"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-06-01T10:00:00Z"),
      registration(ObjectId("000000000000000000000002"), "2026-06-02T10:00:00Z"),
      registration(ObjectId("000000000000000000000003"), "2026-06-03T10:00:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-06-04T10:00:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-06-05T10:00:00Z")
    ],
    createdAt: ISODate("2026-05-20T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000002"),
    title: "AI Ethics Talk",
    description: "Discussion about responsible artificial intelligence and ethical challenges.",
    category: "Talk",
    tags: ["AI", "Ethics", "Technology"],
    startDate: ISODate("2026-07-03T14:00:00Z"),
    endDate: ISODate("2026-07-03T16:00:00Z"),
    capacity: NumberInt(80),
    location: {
      building: "Main Hall",
      room: "A101",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000002"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-06-20T10:00:00Z"),
      registration(ObjectId("000000000000000000000007"), "2026-06-21T10:00:00Z")
    ],
    createdAt: ISODate("2026-05-21T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000003"),
    title: "Cloud Meetup",
    description: "Community meetup about cloud platforms, architecture and modern infrastructure.",
    category: "Meetup",
    tags: ["Cloud", "AWS", "Technology"],
    startDate: ISODate("2026-07-20T18:00:00Z"),
    endDate: ISODate("2026-07-20T20:00:00Z"),
    capacity: NumberInt(50),
    location: {
      building: "Technology Building",
      room: "C301",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000003"),
    registrations: [
      registration(ObjectId("000000000000000000000002"), "2026-07-01T10:00:00Z"),
      registration(ObjectId("000000000000000000000004"), "2026-07-02T10:00:00Z"),
      registration(ObjectId("000000000000000000000008"), "2026-07-03T10:00:00Z"),
      registration(ObjectId("000000000000000000000009"), "2026-07-04T10:00:00Z")
    ],
    createdAt: ISODate("2026-05-22T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000004"),
    title: "Startup Pitch Night",
    description: "Students present innovative startup ideas to a panel and the campus community.",
    category: "Student Activity",
    tags: ["Entrepreneurship", "Career", "Leadership"],
    startDate: ISODate("2026-08-10T18:00:00Z"),
    endDate: ISODate("2026-08-10T21:00:00Z"),
    capacity: NumberInt(100),
    location: {
      building: "Business Center",
      room: "D105",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000007"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-07-20T10:00:00Z"),
      registration(ObjectId("000000000000000000000003"), "2026-07-21T10:00:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-07-22T10:00:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-07-23T10:00:00Z"),
      registration(ObjectId("00000000000000000000000a"), "2026-07-24T10:00:00Z"),
      registration(ObjectId("00000000000000000000000b"), "2026-07-25T10:00:00Z")
    ],
    createdAt: ISODate("2026-05-23T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000005"),
    title: "Yoga and Wellness Session",
    description: "Relaxing campus wellness session focused on movement, breathing and stress management.",
    category: "Student Activity",
    tags: ["Wellness", "Sports"],
    startDate: ISODate("2026-08-25T17:00:00Z"),
    endDate: ISODate("2026-08-25T18:30:00Z"),
    capacity: NumberInt(25),
    location: {
      building: "Sports Center",
      room: "S201",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000008"),
    registrations: [],
    createdAt: ISODate("2026-05-24T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000006"),
    title: "Cybersecurity Awareness",
    description: "Introduction to cybersecurity best practices for students and staff.",
    category: "Talk",
    tags: ["Cybersecurity", "Technology", "Security"],
    startDate: ISODate("2026-09-01T15:00:00Z"),
    endDate: ISODate("2026-09-01T17:00:00Z"),
    capacity: NumberInt(40),
    location: {
      building: "Technology Building",
      room: "C205",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000004"),
    registrations: [
      registration(ObjectId("000000000000000000000002"), "2026-08-15T10:00:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-08-16T10:00:00Z"),
      registration(ObjectId("00000000000000000000000c"), "2026-08-17T10:00:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-08-18T10:00:00Z", "cancelled")
    ],
    createdAt: ISODate("2026-05-25T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000007"),
    title: "Career Networking Evening",
    description: "Networking event connecting students with professionals and recruiters.",
    category: "Career",
    tags: ["Career", "Networking", "Leadership"],
    startDate: ISODate("2026-09-20T18:00:00Z"),
    endDate: ISODate("2026-09-20T20:30:00Z"),
    capacity: NumberInt(50),
    location: {
      building: "Business Center",
      room: "D201",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000009"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-08-20T10:00:00Z"),
      registration(ObjectId("000000000000000000000002"), "2026-08-21T10:00:00Z"),
      registration(ObjectId("000000000000000000000004"), "2026-08-22T10:00:00Z"),
      registration(ObjectId("000000000000000000000007"), "2026-08-23T10:00:00Z"),
      registration(ObjectId("00000000000000000000000a"), "2026-08-24T10:00:00Z"),
      registration(ObjectId("00000000000000000000000b"), "2026-08-25T10:00:00Z", "waiting")
    ],
    createdAt: ISODate("2026-05-26T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000008"),
    title: "Hackathon Kickoff",
    description: "Opening event for a campus hackathon focused on technology and innovation.",
    category: "Hackathon",
    tags: ["Hackathon", "AI", "Technology"],
    startDate: ISODate("2026-10-05T09:00:00Z"),
    endDate: ISODate("2026-10-05T11:00:00Z"),
    capacity: NumberInt(60),
    location: {
      building: "Innovation Center",
      room: "B101",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000006"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-08-26T10:00:00Z"),
      registration(ObjectId("000000000000000000000003"), "2026-08-27T10:00:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-08-28T10:00:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-08-29T10:00:00Z"),
      registration(ObjectId("000000000000000000000008"), "2026-08-30T10:00:00Z"),
      registration(ObjectId("00000000000000000000000c"), "2026-08-31T10:00:00Z")
    ],
    createdAt: ISODate("2026-05-27T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000009"),
    title: "Sustainability Forum",
    description: "Campus discussion about sustainability, climate action and responsible innovation.",
    category: "Talk",
    tags: ["Sustainability", "Environment", "Leadership"],
    startDate: ISODate("2026-10-18T14:00:00Z"),
    endDate: ISODate("2026-10-18T16:00:00Z"),
    capacity: NumberInt(40),
    location: {
      building: "Main Hall",
      room: "A201",
      campus: "Paris"
    },
    organizerId: ObjectId("00000000000000000000000a"),
    registrations: [
      registration(ObjectId("000000000000000000000002"), "2026-09-01T10:00:00Z"),
      registration(ObjectId("000000000000000000000007"), "2026-09-02T10:00:00Z")
    ],
    createdAt: ISODate("2026-05-28T09:00:00Z")
  },

  {
    _id: ObjectId("10000000000000000000000a"),
    title: "Design Thinking Workshop",
    description: "Practical workshop introducing design thinking methods for solving complex problems.",
    category: "Workshop",
    tags: ["Design", "Innovation", "Entrepreneurship"],
    startDate: ISODate("2026-11-07T10:00:00Z"),
    endDate: ISODate("2026-11-07T13:00:00Z"),
    capacity: NumberInt(35),
    location: {
      building: "Business Center",
      room: "D302",
      campus: "Paris"
    },
    organizerId: ObjectId("00000000000000000000000b"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-09-03T10:00:00Z"),
      registration(ObjectId("000000000000000000000004"), "2026-09-03T11:00:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-09-04T10:00:00Z"),
      registration(ObjectId("000000000000000000000009"), "2026-09-04T11:00:00Z")
    ],
    createdAt: ISODate("2026-05-29T09:00:00Z")
  },

  {
    _id: ObjectId("10000000000000000000000b"),
    title: "Cultural Night",
    description: "An evening celebrating cultures, music, food and creativity across the campus community.",
    category: "Student Activity",
    tags: ["Arts", "Culture", "Community"],
    startDate: ISODate("2026-11-20T18:00:00Z"),
    endDate: ISODate("2026-11-20T22:00:00Z"),
    capacity: NumberInt(120),
    location: {
      building: "Main Hall",
      room: "Grand Hall",
      campus: "Paris"
    },
    organizerId: ObjectId("00000000000000000000000c"),
    registrations: [],
    createdAt: ISODate("2026-05-30T09:00:00Z")
  },

  {
    _id: ObjectId("10000000000000000000000c"),
    title: "Cloud Architecture Talk",
    description: "Exploration of scalable cloud architectures and modern distributed systems.",
    category: "Talk",
    tags: ["Cloud", "Architecture", "Technology"],
    startDate: ISODate("2026-12-04T15:00:00Z"),
    endDate: ISODate("2026-12-04T17:00:00Z"),
    capacity: NumberInt(70),
    location: {
      building: "Technology Building",
      room: "C301",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000003"),
    registrations: [
      registration(ObjectId("000000000000000000000002"), "2026-09-05T10:00:00Z"),
      registration(ObjectId("000000000000000000000003"), "2026-09-05T11:00:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-09-05T12:00:00Z")
    ],
    createdAt: ISODate("2026-05-31T09:00:00Z")
  },

  {
    _id: ObjectId("10000000000000000000000d"),
    title: "Student Leadership Meetup",
    description: "Meetup for students interested in leadership, community building and campus initiatives.",
    category: "Meetup",
    tags: ["Leadership", "Student", "Community"],
    startDate: ISODate("2027-01-15T17:00:00Z"),
    endDate: ISODate("2027-01-15T19:00:00Z"),
    capacity: NumberInt(30),
    location: {
      building: "Student Center",
      room: "E102",
      campus: "Paris"
    },
    organizerId: ObjectId("00000000000000000000000d"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-09-05T13:00:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-09-05T14:00:00Z"),
      registration(ObjectId("000000000000000000000007"), "2026-09-05T15:00:00Z"),
      registration(ObjectId("000000000000000000000008"), "2026-09-05T16:00:00Z"),
      registration(ObjectId("00000000000000000000000a"), "2026-09-05T17:00:00Z")
    ],
    createdAt: ISODate("2026-06-01T09:00:00Z")
  },

  {
    _id: ObjectId("10000000000000000000000e"),
    title: "Machine Learning Lab",
    description: "Practical laboratory session exploring machine learning workflows and Python tools.",
    category: "Workshop",
    tags: ["AI", "Machine Learning", "Python"],
    startDate: ISODate("2027-01-28T10:00:00Z"),
    endDate: ISODate("2027-01-28T13:00:00Z"),
    capacity: NumberInt(20),
    location: {
      building: "Innovation Center",
      room: "B305",
      campus: "Paris"
    },
    organizerId: ObjectId("00000000000000000000000e"),
    registrations: [
      registration(ObjectId("000000000000000000000002"), "2026-09-05T18:00:00Z"),
      registration(ObjectId("000000000000000000000004"), "2026-09-05T19:00:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-09-05T20:00:00Z"),
      registration(ObjectId("000000000000000000000009"), "2026-09-05T21:00:00Z")
    ],
    createdAt: ISODate("2026-06-02T09:00:00Z")
  },

  {
    _id: ObjectId("10000000000000000000000f"),
    title: "Entrepreneurship Masterclass",
    description: "Masterclass covering startup strategy, business models and entrepreneurial skills.",
    category: "Career",
    tags: ["Entrepreneurship", "Career", "Business"],
    startDate: ISODate("2027-02-10T15:00:00Z"),
    endDate: ISODate("2027-02-10T17:00:00Z"),
    capacity: NumberInt(50),
    location: {
      building: "Business Center",
      room: "D401",
      campus: "Paris"
    },
    organizerId: ObjectId("00000000000000000000000f"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-09-05T22:00:00Z"),
      registration(ObjectId("000000000000000000000003"), "2026-09-05T23:00:00Z")
    ],
    createdAt: ISODate("2026-06-03T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000010"),
    title: "Campus Sports Tournament",
    description: "Team sports tournament bringing students together for a friendly competition.",
    category: "Sports",
    tags: ["Sports", "Wellness", "Teamwork"],
    startDate: ISODate("2027-02-21T09:00:00Z"),
    endDate: ISODate("2027-02-21T17:00:00Z"),
    capacity: NumberInt(12),
    location: {
      building: "Sports Center",
      room: "Court 1",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000008"),
    registrations: [
      registration(ObjectId("000000000000000000000001"), "2026-09-06T08:00:00Z"),
      registration(ObjectId("000000000000000000000002"), "2026-09-06T08:01:00Z"),
      registration(ObjectId("000000000000000000000003"), "2026-09-06T08:02:00Z"),
      registration(ObjectId("000000000000000000000004"), "2026-09-06T08:03:00Z"),
      registration(ObjectId("000000000000000000000005"), "2026-09-06T08:04:00Z"),
      registration(ObjectId("000000000000000000000006"), "2026-09-06T08:05:00Z"),
      registration(ObjectId("000000000000000000000007"), "2026-09-06T08:06:00Z"),
      registration(ObjectId("000000000000000000000008"), "2026-09-06T08:07:00Z"),
      registration(ObjectId("000000000000000000000009"), "2026-09-06T08:08:00Z"),
      registration(ObjectId("00000000000000000000000a"), "2026-09-06T08:09:00Z"),
      registration(ObjectId("00000000000000000000000b"), "2026-09-06T08:10:00Z"),
      registration(ObjectId("00000000000000000000000c"), "2026-09-06T08:11:00Z")
    ],
    createdAt: ISODate("2026-06-04T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000011"),
    title: "Research Showcase",
    description: "Showcase of student and faculty research projects across different disciplines.",
    category: "Student Activity",
    tags: ["Research", "Innovation", "Technology"],
    startDate: ISODate("2026-09-25T14:00:00Z"),
    endDate: ISODate("2026-09-25T17:00:00Z"),
    capacity: NumberInt(45),
    location: {
      building: "Research Building",
      room: "R101",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000005"),
    registrations: [],
    createdAt: ISODate("2026-06-05T09:00:00Z")
  },

  {
    _id: ObjectId("100000000000000000000012"),
    title: "Open Source Meetup",
    description: "Community meetup discussing open source projects, contribution and collaboration.",
    category: "Meetup",
    tags: ["Open Source", "Technology", "Community"],
    startDate: ISODate("2026-10-30T18:00:00Z"),
    endDate: ISODate("2026-10-30T20:00:00Z"),
    capacity: NumberInt(40),
    location: {
      building: "Technology Building",
      room: "C102",
      campus: "Paris"
    },
    organizerId: ObjectId("000000000000000000000006"),
    registrations: [
      registration(ObjectId("000000000000000000000003"), "2026-09-06T09:00:00Z"),
      registration(ObjectId("000000000000000000000007"), "2026-09-06T09:01:00Z"),
      registration(ObjectId("000000000000000000000008"), "2026-09-06T09:02:00Z"),
      registration(ObjectId("00000000000000000000000c"), "2026-09-06T09:03:00Z")
    ],
    createdAt: ISODate("2026-06-06T09:00:00Z")
  }
];

campusDB.events.insertMany(events);


// ------------------------------------------------------------
// SEED SUMMARY
// ------------------------------------------------------------

const registrationStats = campusDB.events.aggregate([
  {
    $project: {
      registrationCount: { $size: "$registrations" }
    }
  },
  {
    $group: {
      _id: null,
      totalRegistrations: { $sum: "$registrationCount" }
    }
  }
]).toArray();

const totalRegistrations =
  registrationStats.length > 0
    ? registrationStats[0].totalRegistrations
    : 0;

const categories = campusDB.events.distinct("category");
const tags = campusDB.events.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags" } },
  { $count: "tagCount" }
]).toArray();

const tagCount = tags.length > 0 ? tags[0].tagCount : 0;

print("======================================");
print("Campus Event Manager - Seed Complete");
print("======================================");
print("Users: " + campusDB.users.countDocuments());
print("Events: " + campusDB.events.countDocuments());
print("Categories: " + categories.length);
print("Unique tags: " + tagCount);
print("Total registrations: " + totalRegistrations);
print("======================================");