# Campus Event Manager

A web application developed for the MSc Data Engineering & Cloud Computing NoSQL project[cite: 1]. The platform leverages MongoDB to manage campus users, event schedules, registrations, and real-time event analytics[cite: 1].

---

## 1. Project Overview

This project demonstrates core NoSQL and document-database concepts[cite: 1]:
- Document-oriented data modeling[cite: 1]
- Embedded documents and array manipulation[cite: 1]
- Referenced relationships using `ObjectId`[cite: 1]
- Schema validation and unique indexing[cite: 1]
- CRUD operations, query filters, and projections[cite: 1]
- Multi-stage MongoDB Aggregation Pipelines[cite: 1]

---

## 2. Tech Stack

- **Backend:** Python 3.14, Flask, Jinja2, python-dotenv[cite: 1]
- **Database:** MongoDB, PyMongo, MongoDB Shell (`mongosh`)[cite: 1]
- **Frontend:** HTML5, CSS3[cite: 1]

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
```[cite: 1]

---

## 4. Database Architecture

- **Database Name:** `campus_events`[cite: 1]
- **Default Connection URI:** `mongodb://127.0.0.1:27017`[cite: 1]
- **Collections:** `users`, `events`[cite: 1]

### Data Models

#### `users` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `_id` | ObjectId | Unique identifier[cite: 1] |
| `firstName` | String | User's first name[cite: 1] |
| `lastName` | String | User's last name[cite: 1] |
| `email` | String | Unique email address (indexed)[cite: 1] |
| `department` | String | Academic/administrative department[cite: 1] |
| `role` | String | Assigned role[cite: 1] |
| `interests` | Array | List of interest tags[cite: 1] |
| `createdAt` | Date | Record creation timestamp[cite: 1] |

#### `events` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `_id` | ObjectId | Unique identifier[cite: 1] |
| `title` | String | Event title[cite: 1] |
| `description`| String | Event description[cite: 1] |
| `category` | String | Event category (indexed)[cite: 1] |
| `tags` | Array | Associated tag labels[cite: 1] |
| `startDate` | Date | Event start date/time (indexed)[cite: 1] |
| `endDate` | Date | Event end date/time[cite: 1] |
| `capacity` | Number | Maximum participant limit[cite: 1] |
| `location` | Object | **Embedded document** containing location details[cite: 1] |
| `organizerId` | ObjectId | **Reference** to the user organizing the event[cite: 1] |
| `registrations`| Array | **Embedded documents** containing registration records[cite: 1] |
| `createdAt` | Date | Record creation timestamp[cite: 1] |

**Embedded Registration Subdocument:**
- `userId` (ObjectId): Reference to registered user[cite: 1]
- `registeredAt` (Date): Registration timestamp[cite: 1]
- `status` (String): Registration state (e.g., confirmed, cancelled)[cite: 1]

### Database Indexes
Created via `database/init.js`:
- `users.email` (Unique): Enforces email uniqueness across users[cite: 1].
- `events.startDate`: Optimizes chronologically sorted queries[cite: 1].
- `events.category`: Optimizes category-based filtering[cite: 1].

---

## 5. Installation & Setup

### Prerequisites
- Python 3.14+[cite: 1]
- Local MongoDB Server running on port `27017`[cite: 1]
- MongoDB Shell (`mongosh`) installed[cite: 1]

### Step 1: Clone Repository
```powershell
git clone [https://github.com/Kavyamona7/campus-event-manager.git](https://github.com/Kavyamona7/campus-event-manager.git)
cd campus-event-manager
```[cite: 1]

### Step 2: Virtual Environment Setup
```powershell
# Create virtual environment
python -m venv .venv

# Activate on Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Install requirements
python -m pip install -r requirements.txt
```[cite: 1]

### Step 3: Configure Environment Variables
Create a `.env` file in the project root[cite: 1]:
```env
MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DB_NAME=campus_events
```[cite: 1]

### Step 4: Initialize & Seed Database
Ensure your MongoDB daemon is running, then run[cite: 1]:
```powershell
# Run schema validation setup and create collections/indexes
mongosh database/init.js

# Populate dataset (15 users, 18 events, 40+ registrations)
mongosh database/seed.js
```[cite: 1]

### Step 5: Run the Application
```powershell
python src/app.py
```[cite: 1]

Access the web interface at: **`http://127.0.0.1:5000/`**[cite: 1]

---

## 6. Application Modules

### **Dashboard**
- Global statistics: Total users, total events, upcoming event counts, and total registrations[cite: 1].
- Quick preview of the next 5 upcoming events[cite: 1].
- Highlights the most popular event by confirmed attendee count[cite: 1].

### **Events**
- Search and multi-criteria filtering (by title, category, tag, upcoming/past, and dates)[cite: 1].
- Visual capacity indicator with real-time confirmed attendee counts[cite: 1].
- Full CRUD interface (Create, Read, Update, Delete events)[cite: 1].

### **Event Details & Registrations**
- Displays embedded location details, organizer metadata, and capacity metrics[cite: 1].
- Real-time occupancy percentage calculation[cite: 1].
- **Atomic Operations:** Uses `$push` to register and `$pull` to cancel registrations[cite: 1].
- **Validation Rules:** Blocks duplicate sign-ups and enforces maximum capacity constraints[cite: 1].

### **Users**
- Search directory by name or email, with department and role filters[cite: 1].
- User profile detailing registered events, attendance statuses, and historical data[cite: 1].
- Full user CRUD management with referential integrity checks before deletion[cite: 1].

### **Analytics (Aggregation Pipelines)**
Advanced aggregation pipelines computing real-time analytics[cite: 1]:
1. **Registrations by Category:** Aggregates event totals and confirmed seats per category[cite: 1].
2. **Top 5 Events:** Highlights highest registrations and occupancy percentages[cite: 1].
3. **Users With No Registration:** Identifies inactive campus accounts[cite: 1].
4. **Events Above Average Occupancy:** Pinpoints high-performing events using computed averages[cite: 1].
5. **Most Used Tags:** Evaluates tag distribution using `$unwind` and grouping[cite: 1].
6. **Events by Month:** Historical breakdown by year and month using `$year` and `$month` operators[cite: 1].

---

## 7. Security & Error Handling

- **Database-Level Guardrails:** MongoDB JSON Schema validation enforces field types, constraints, and valid dates[cite: 1].
- **Referential Safeguards:** Blocks user deletion if that user is associated with active event registrations[cite: 1].
- **Input Sanitization:** Validates emails, required inputs, ObjectId formats, and ensures end dates do not precede start dates[cite: 1].
- **Secret Isolation:** `.env`, `.venv/`, and Python cache artifacts are permanently excluded via `.gitignore`[cite: 1].

---

## 8. Documentation & Author

- **Technical Report:** Complete architectural analysis, modeling decisions, and page screenshots are available in [`report/project-report.pdf`](report/project-report.pdf)[cite: 1].
- **Author:** Kavya Basappa[cite: 1]
- **Program:** MSc Data Engineering & Cloud Computing[cite: 1]