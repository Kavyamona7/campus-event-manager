CAMPUS EVENT MANAGER 

1. Project Overview

Campus Event Manager is a small web application developed as part of the MSc Data Engineering & Cloud Computing NoSQL project.

The application uses MongoDB to manage campus users, events, registrations and event analytics.

The project demonstrates MongoDB document modeling, CRUD operations, embedded documents, references, indexes and aggregation pipelines.

2. Technologies

- Python 3.14
- Flask
- PyMongo
- MongoDB
- MongoDB Shell (mongosh)
- HTML / CSS
- Jinja2
- python-dotenv


3. Project Structure

campus-event-manager/
│
├── database/
│   ├── init.js
│   └── seed.js
│
├── report/
│   └── project-report.pdf
│
├── src/
│   ├── routes/
│   │   ├── analytics.py
│   │   ├── dashboard.py
│   │   ├── events.py
│   │   └── users.py
│   │
│   ├── services/
│   │   ├── analytics_service.py
│   │   ├── dashboard_service.py
│   │   ├── event_service.py
│   │   ├── mongo_service.py
│   │   └── user_service.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── analytics/
│   │   ├── events/
│   │   ├── users/
│   │   ├── base.html
│   │   └── dashboard.html
│   │
│   ├── app.py
│   └── config.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt

4. Database

The application uses the following MongoDB database: campus_events

The database contains two main collections:

users
events

MongoDB is configured locally by default: mongodb://127.0.0.1:27017
Data Model
Users

Each user contains:

_id
firstName
lastName
email
department
role
interests
createdAt

The email field has a unique index.

5. Events

Each event contains:

_id
title
description
category
tags
startDate
endDate
capacity
location
organizerId
registrations
createdAt

The location is embedded inside the event document.

The registrations array contains embedded registration documents with:

userId
registeredAt
status

The event organizer is referenced using organizerId.

Installation

a. Clone the repository
git clone <https://github.com/Kavyamona7>
cd campus-event-manager

b. Create a virtual environment

On Windows PowerShell: python -m venv .venv

Activate the environment:  .\.venv\Scripts\Activate.ps1

c. Install dependencies: python -m pip install -r requirements.txt
MongoDB Configuration

Create a .env file in the project root:

MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DB_NAME=campus_events

The .env file is excluded from Git using .gitignore.

d. Initialize the Database

Make sure the MongoDB server is running.

From the project root, run: mongosh database/init.js

The initialization script:

Creates the campus_events database
Creates the users collection
Creates the events collection
Applies MongoDB validation rules
Creates the required indexes
Seed the Database

Run: mongosh database/seed.js

The seed script inserts sample users, events and registrations.

The dataset contains:

15 users
18 events
Multiple event categories
Multiple tags
40+ registrations
Future and past events
Events with zero registrations
A full-capacity event

The seed script is reproducible and can be executed again after database initialization.

5. Run the Application

Activate the virtual environment:  .\.venv\Scripts\Activate.ps1

Start the Flask application: python src/app.py

Open the application in a browser: http://127.0.0.1:5000/

Application Pages that are visible are:
 
1. Dashboard

The Dashboard displays:

Total number of users
Total number of events
Number of upcoming events
Total registrations
Next five upcoming events
Most popular event based on confirmed registrations

All information is retrieved from MongoDB.

2. Events

The Events page provides:

Complete event listing
Search by title
Category filtering
Tag filtering
Upcoming/past filtering
Date sorting
Capacity indicators
Confirmed registration count
Create event
Edit event
Delete event
Event details
3. Event Details & Registrations

The Event Details page provides:

Event description
Category
Tags
Start and end dates
Embedded location
Organizer information
Capacity
Confirmed registration count
Occupancy percentage
Participant list
User registration

Registration rules include:

Existing users can be registered
Duplicate registrations are prevented
Registration is rejected when the event is full
Registrations can be cancelled
Participant information updates immediately

MongoDB array operations such as $push and $pull are used to update embedded registrations.

4. Users

The Users page provides:

User directory
Search by name or email
Department filtering
Role filtering
Registration count
Create user
Edit user
Delete user
User details

The user details page displays:

Personal information
Interests
Registered events
Registration status
Upcoming registration count
Past registration count

Users with zero registrations are also supported.

5. Analytics

The Analytics page contains six MongoDB aggregation analyses:

A. Registrations by Category

Displays:

Category
Number of events
Total confirmed registrations
B. Top 5 Events

Displays:

Event title
Category
Capacity
Confirmed registrations
Occupancy percentage
C. Users With No Registration

Identifies users who are not registered for any event.

D. Events Above Average Occupancy

Calculates the average event occupancy and identifies events whose occupancy is above the average.

E. Most Used Tags

Calculates how frequently each event tag is used.

F. Events by Month

Displays:

Year
Month
Number of events
Confirmed registrations
MongoDB Features Demonstrated

The project demonstrates the following MongoDB concepts:

Document-oriented data modeling
Embedded documents
Arrays
References using ObjectId
Schema validation
Unique indexes
CRUD operations
Query filters
Regular expressions
Sorting
Projection
$push
$pull
$filter
$unwind
$group
$lookup
$match
$project
$sort
$limit
$addFields
$avg
$year
$month
Multi-stage aggregation pipelines
Indexes

The following indexes are created by database/init.js:

Users
users.email

Unique index preventing duplicate email addresses.

Events
events.startDate
events.category

These indexes improve event filtering and sorting operations.

Validation and Error Handling

The application handles several invalid operations, including:

Duplicate email addresses
Invalid email format
Empty required fields
Invalid capacity
End date before start date
Invalid ObjectId
Non-existent event
Non-existent user
Duplicate event registration
Registration when an event is full
Attempting to delete a user referenced by event registrations

MongoDB validation is also applied at database level.

Security and Configuration

Sensitive configuration is stored in .env.

The following files and directories are excluded from Git:

.env
.venv/
__pycache__/
*.pyc

No passwords, API keys or other secrets are committed to the repository.

Report

The technical project report is available in:

report/project-report.pdf

The report contains:

Project overview
NoSQL data model
Modeling decisions
Application architecture
Screenshots of the five application pages
MongoDB aggregation analysis
Conclusion and possible improvements

Author
Kavya Basappa
MSc Data Engineering & Cloud Computing