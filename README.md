# Campus Event Manager

A web application developed for the MSc Data Engineering & Cloud Computing NoSQL project. The platform leverages MongoDB to manage campus users, event schedules, registrations, and real-time event analytics.

---

## 1. Project Overview

This project demonstrates core NoSQL and document-database concepts:
- Document-oriented data modeling
- Embedded documents and array manipulation
- Referenced relationships using `ObjectId`
- Schema validation and unique indexing
- CRUD operations, query filters, and projections
- Multi-stage MongoDB Aggregation Pipelines

---

## 2. Tech Stack

- **Backend:** Python 3.14, Flask, Jinja2, python-dotenv
- **Database:** MongoDB, PyMongo, MongoDB Shell (`mongosh`)
- **Frontend:** HTML5, CSS3

---

## 3. Project Structure

```text
campus-event-manager/
├── database/
│   ├── init.js
│   └── seed.js
├── report/
│   └── project-report.pdf
├── src/
│   ├── routes/
│   │   ├── analytics.py
│   │   ├── dashboard.py
│   │   ├── events.py
│   │   └── users.py
│   ├── services/
│   │   ├── analytics_service.py
│   │   ├── dashboard_service.py
│   │   ├── event_service.py
│   │   └── user_service.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   └── dashboard.html
│   └── app.py
├── .env
├── .gitignore
├── config.py
├── README.md
└── requirements.txt
```

---

## 4. Database Architecture

- **Database Name:** `campus_events`
- **Default Connection URI:** `mongodb://127.0.0.1:27017`
- **Collections:** `users`, `events`

### Data Models

#### `users` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `_id` | ObjectId | Unique identifier |
| `firstName` | String | User's first name |
| `lastName` | String | User's last name |
| `email` | String | Unique email address (indexed) |
| `department` | String | Academic/administrative department |
| `role` | String | Assigned role |
| `interests` | Array | List of interest tags |
| `createdAt` | Date | Record creation timestamp |

#### `events` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `_id` | ObjectId | Unique identifier |
| `title` | String | Event title |
| `description`| String | Event description |
| `category` | String | Event category (indexed) |
| `tags` | Array | Associated tag labels |
| `startDate` | Date | Event start date/time (indexed) |
| `endDate` | Date | Event end date/time |
| `capacity` | Number | Maximum participant limit |
| `location` | Object | **Embedded document** containing location details |
| `organizerId` | ObjectId | **Reference** to the user organizing the event |
| `registrations`| Array | **Embedded documents** containing registration records |
| `createdAt` | Date | Record creation timestamp |

**Embedded Registration Subdocument:**
- `userId` (ObjectId): Reference to registered user
- `registeredAt` (Date): Registration timestamp
- `status` (String): Registration state (e.g., confirmed, cancelled)

### Database Indexes
Created via `database/init.js`:
- `users.email` (Unique): Enforces email uniqueness across users.
- `events.startDate`: Optimizes chronologically sorted queries.
- `events.category`: Optimizes category-based filtering.

---

## 5. Installation & Setup

### Prerequisites
- Python 3.14+
- Local MongoDB Server running on port `27017`
- MongoDB Shell (`mongosh`) installed

### Step 1: Clone Repository
```powershell
git clone [https://github.com/Kavyamona7/campus-event-manager.git](https://github.com/Kavyamona7/campus-event-manager.git)
cd campus-event-manager
```

### Step 2: Virtual Environment Setup
```powershell
# Create virtual environment
python -m venv .venv

# Activate on Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Install requirements
python -m pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the project root:
```env
MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DB_NAME=campus_events
```

### Step 4: Initialize & Seed Database
Ensure your MongoDB daemon is running, then run:
```powershell
# Run schema validation setup and create collections/indexes
mongosh database/init.js

# Populate dataset (15 users, 18 events, 40+ registrations)
mongosh database/seed.js
```

### Step 5: Run the Application
```powershell
python src/app.py
```

Access the web interface at: **`http://127.0.0.1:5000/`**

---

## 6. Application Modules

### **Dashboard**
- Global statistics: Total users, total events, upcoming event counts, and total registrations.
- Quick preview of the next 5 upcoming events.
- Highlights the most popular event by confirmed attendee count.

### **Events**
- Search and multi-criteria filtering (by title, category, tag, upcoming/past, and dates).
- Visual capacity indicator with real-time confirmed attendee counts.
- Full CRUD interface (Create, Read, Update, Delete events).

### **Event Details & Registrations**
- Displays embedded location details, organizer metadata, and capacity metrics.
- Real-time occupancy percentage calculation.
- **Atomic Operations:** Uses `$push` to register and `$pull` to cancel registrations.
- **Validation Rules:** Blocks duplicate sign-ups and enforces maximum capacity constraints.

### **Users**
- Search directory by name or email, with department and role filters.
- User profile detailing registered events, attendance statuses, and historical data.
- Full user CRUD management with referential integrity checks before deletion.

### **Analytics (Aggregation Pipelines)**
Advanced aggregation pipelines computing real-time analytics:
1. **Registrations by Category:** Aggregates event totals and confirmed seats per category.
2. **Top 5 Events:** Highlights highest registrations and occupancy percentages.
3. **Users With No Registration:** Identifies inactive campus accounts.
4. **Events Above Average Occupancy:** Pinpoints high-performing events using computed averages.
5. **Most Used Tags:** Evaluates tag distribution using `$unwind` and grouping.
6. **Events by Month:** Historical breakdown by year and month using `$year` and `$month` operators.

---

## 7. Security & Error Handling

- **Database-Level Guardrails:** MongoDB JSON Schema validation enforces field types, constraints, and valid dates.
- **Referential Safeguards:** Blocks user deletion if that user is associated with active event registrations.
- **Input Sanitization:** Validates emails, required inputs, ObjectId formats, and ensures end dates do not precede start dates.
- **Secret Isolation:** `.env`, `.venv/`, and Python cache artifacts are permanently excluded via `.gitignore`.

---

## 8. Documentation & Author

- **Technical Report:** Complete architectural analysis, modeling decisions, and page screenshots are available in [`report/project-report.pdf`](report/project-report.pdf).
- **Author:** Kavya Basappa
- **Program:** MSc Data Engineering & Cloud Computing
