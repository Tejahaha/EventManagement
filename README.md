# EventHub — Event Management System

> A full-featured Django-based Event Management System built as a PFSD Academic Project.
> Organizers create and manage events. Participants discover, register, pay, and attend. Admins oversee everything.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [User Roles & Permissions](#user-roles--permissions)
- [Authentication System](#authentication-system)
- [Event Management](#event-management)
- [Registration System](#registration-system)
- [Payment System](#payment-system)
- [Attendance System](#attendance-system)
- [Feedback System](#feedback-system)
- [Dashboard System](#dashboard-system)
- [Search & Filter](#search--filter)
- [CSV Export](#csv-export)
- [Email Notifications](#email-notifications)
- [Admin Panel](#admin-panel)
- [Database Models & Relationships](#database-models--relationships)
- [URL Structure](#url-structure)
- [Sample Data](#sample-data)
- [Key Validations](#key-validations)

---

## Project Overview

**EventHub** is a web-based Event Management System where:

- **Organizers** can create, edit, delete events and manage registrations and attendance
- **Participants** can discover events, register, pay, track attendance, and leave feedback
- **Admins** have full oversight of the entire system with system-wide stats

Built with **Django 6.0.4**, **SQLite**, **Bootstrap 5**, and **Matplotlib**.

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend Framework | Django 6.0.4 |
| Database | SQLite (`db.sqlite3`) |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Image Handling | Pillow |
| Charts | Matplotlib (rendered as base64 PNG) |
| Authentication | Django built-in auth system |
| Forms | Django ModelForms |
| Templating | Django Templates |
| Static Files | Django staticfiles |
| Media Uploads | Django media handling |

---

## Project Structure

```
EventManagement/
│
├── EventManagement/           ← Main project config
│   ├── settings.py            ← All settings, email config placeholder
│   ├── urls.py                ← Root URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  ← User auth & profiles
│   ├── models.py              ← CustomUser model
│   ├── views.py               ← register, login, logout, profile
│   ├── forms.py               ← RegisterForm, LoginForm, ProfileUpdateForm
│   ├── urls.py
│   └── admin.py
│
├── events/                    ← Core event module
│   ├── models.py              ← Category, Event
│   ├── views.py               ← CRUD + search/filter + CSV export
│   ├── forms.py               ← EventForm, CategoryForm
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/
│       └── seed_data.py       ← Sample data loader
│
├── registrations/             ← Event registration
│   ├── models.py              ← Registration
│   ├── views.py               ← register, cancel, my registrations
│   └── urls.py
│
├── payments/                  ← Payment tracking
│   ├── models.py              ← Payment
│   ├── views.py               ← payment page, payment history
│   └── urls.py
│
├── attendance/                ← Attendance tracking
│   ├── models.py              ← Attendance
│   ├── views.py               ← mark attendance, attendance history
│   └── urls.py
│
├── feedback/                  ← Ratings & reviews
│   ├── models.py              ← Feedback
│   ├── views.py               ← submit feedback
│   ├── forms.py               ← FeedbackForm
│   └── urls.py
│
├── dashboard/                 ← Role-based dashboards
│   ├── views.py               ← admin/organizer/participant dashboards
│   └── urls.py
│
├── templates/                 ← All HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── events/
│   ├── registrations/
│   ├── payments/
│   ├── attendance/
│   ├── feedback/
│   └── dashboard/
│
├── static/
│   └── css/custom.css         ← Custom styles
│
├── media/                     ← Uploaded files (banners, profile pics)
├── manage.py
└── db.sqlite3                 ← SQLite database
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- pip

### Steps

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd EventManagement
```

**2. Create and activate virtual environment**

```bash
python -m venv .venv

# Windows CMD / PowerShell
.venv\Scripts\activate

# Windows Git Bash / Mac / Linux
source .venv/Scripts/activate
```

**3. Install dependencies**

```bash
pip install django pillow matplotlib
```

**4. Configure email (optional)**

Open `EventManagement/settings.py` and fill in your Gmail credentials at the bottom:

```python
EMAIL_HOST_USER = 'YOUR_EMAIL@gmail.com'     # ← your Gmail address
EMAIL_HOST_PASSWORD = 'YOUR_APP_PASSWORD'    # ← Gmail App Password
```

> **Note:** Email is optional. The app works fully without it. Emails fail silently if not configured.
>
> To get a Gmail App Password: Google Account → Security → 2-Step Verification → App Passwords → Generate.

**5. Run migrations**

```bash
python manage.py migrate
```

**6. Load sample data**

```bash
python manage.py seed_data
```

This creates:
- 6 categories (Technology, Music, Sports, Workshop, Conference, Art)
- 2 test users (`organizer1` and `user1`)
- 3 sample events

**7. Create admin account**

```bash
python manage.py createsuperuser
```

---

## How to Run

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000/**

### Quick Access URLs

| Page | URL |
|---|---|
| Home | http://127.0.0.1:8000/ |
| Browse Events | http://127.0.0.1:8000/events/ |
| Login | http://127.0.0.1:8000/accounts/login/ |
| Register | http://127.0.0.1:8000/accounts/register/ |
| Dashboard | http://127.0.0.1:8000/dashboard/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

### Pre-loaded Test Accounts

| Username | Password | Role |
|---|---|---|
| `organizer1` | `organizer123` | Organizer |
| `user1` | `user12345` | Participant |
| *(your superuser)* | *(you set it)* | Admin |

---

## User Roles & Permissions

There are **3 roles** in the system. Every user has exactly one role.

### Admin
- Created via `python manage.py createsuperuser`
- Full access to everything in the system
- Can view, edit, delete **any** event regardless of organizer
- Access to Django Admin panel at `/admin/`
- Sees the **Admin Dashboard** with system-wide statistics
- Can export CSV and mark attendance for any event

### Organizer
- Selected during registration ("Organizer" option)
- Can **create** new events
- Can **edit** and **delete** only their own events
- Can **mark attendance** for their own events
- Can **export CSV** of registrations for their own events
- Sees the **Organizer Dashboard** with personal event stats and charts

### Participant (default)
- Default role during registration
- Can **browse** all events
- Can **register** for and **cancel** registrations
- Can **pay** for paid events
- Can **view** their own attendance history
- Can **leave feedback** only for completed events they attended
- Sees the **Participant Dashboard** with personal stats

### How Role Checking Works

**In models:**
```python
def is_admin(self):       return self.role == 'admin'
def is_organizer(self):   return self.role == 'organizer'
def is_participant(self):  return self.role == 'participant'
```

**In views:**
```python
if not request.user.is_organizer() and not request.user.is_admin():
    messages.error(request, 'Only organizers can create events.')
    return redirect('events:list')
```

**In templates:**
```html
{% if user.is_organizer or user.is_admin %}
    <a href="{% url 'events:create' %}">Create Event</a>
{% endif %}
```

---

## Authentication System

### Registration (`/accounts/register/`)
- Fields: Username, Email, Phone, Role (Participant or Organizer), Password, Confirm Password
- Password is **automatically hashed** by Django — never stored as plain text
- After registration, user is **auto-logged in** and redirected to dashboard
- Admin role is only assignable via the Django admin panel

### Login (`/accounts/login/`)
- On success: redirected to `/dashboard/` or the `?next=` URL if redirected from a protected page
- On failure: flash error message shown
- All protected views use `@login_required` decorator

### Logout (`/accounts/logout/`)
- Clears the session and redirects to login page

### Profile (`/accounts/profile/`)
- Edit: Username, Email, Phone, Bio, Profile Image
- Profile image stored in `media/profile_images/`

### CSRF Protection
- Every form includes `{% csrf_token %}` — Django middleware blocks any submission without a valid token

---

## Event Management

### Event Fields

| Field | Type | Description |
|---|---|---|
| `organizer` | ForeignKey → CustomUser | Who created this event |
| `category` | ForeignKey → Category | Event category |
| `title` | CharField | Event name |
| `description` | TextField | Full description |
| `venue` | CharField | Location |
| `banner` | ImageField | Stored in `media/event_banners/` |
| `date` | DateField | Event date |
| `time` | TimeField | Event time |
| `total_seats` | PositiveIntegerField | Maximum capacity |
| `available_seats` | PositiveIntegerField | Decreases on each registration |
| `ticket_price` | DecimalField | `0.00` = Free event |
| `status` | CharField | upcoming / ongoing / completed / cancelled |
| `created_at` | DateTimeField | Auto-set on creation |

### Event Status Options

| Status | Description |
|---|---|
| `upcoming` | Not started yet, registration open |
| `ongoing` | Currently happening, registration still open |
| `completed` | Over, feedback can now be submitted |
| `cancelled` | No registration allowed |

### Create Event (`/events/create/`)
- Only Organizers and Admins can access
- Event date **cannot be in the past**
- Total seats must be > 0
- `available_seats` is automatically set equal to `total_seats` on creation

### Edit Event (`/events/<pk>/edit/`)
- Only the event's organizer or an Admin can edit
- Seat adjustment is handled automatically when `total_seats` changes

### Delete Event (`/events/<pk>/delete/`)
- Only the event's organizer or an Admin can delete
- Shows a confirmation page before deletion
- All related registrations, payments, attendance, and feedback are also deleted (CASCADE)

### Browse Events (`/events/`)
- Public page — no login required
- Search + filter bar at the top
- Event cards show: banner, title, category, date, venue, price, seats left, status

### Event Detail (`/events/<pk>/`)
- Public page
- Full event info with seat availability progress bar
- Shows average star rating and all reviews
- Participants see Register / Cancel button
- Organizers/Admins see Edit / Delete / Mark Attendance / Export CSV buttons

---

## Registration System

### Registration Fields

| Field | Type | Description |
|---|---|---|
| `user` | ForeignKey → CustomUser | Who registered |
| `event` | ForeignKey → Event | Which event |
| `registration_id` | CharField | Auto-generated (`REG-XXXXXXXX`) |
| `registered_at` | DateTimeField | Auto-set on creation |
| `status` | CharField | active / cancelled |

### Registration Flow (`/registrations/event/<pk>/register/`)

1. User clicks "Register Now" on the event detail page
2. System checks in order:
   - Event status is `completed` or `cancelled` → blocked
   - `available_seats == 0` → blocked with "Fully Booked"
   - User already has an `active` registration → blocked with "Already registered"
   - User has a `cancelled` registration → **re-registration allowed** (record reactivated)
3. `Registration` object created with auto-generated ID
4. `event.available_seats` decremented by 1
5. `Payment` object created automatically:
   - Free event → `payment_status = 'paid'` immediately
   - Paid event → `payment_status = 'pending'`
6. Confirmation email sent (silently skipped if email not configured)
7. Free event → redirected to My Registrations
8. Paid event → redirected to Payment page

### Cancel Registration (`/registrations/<pk>/cancel/`)
- Sets `registration.status = 'cancelled'`
- Increments `event.available_seats` by 1 (seat is freed)

### Registration ID Format
```
REG-A3F9B2C1
```
Generated using Python `uuid4`, prefixed with `REG-`.

---

## Payment System

### Payment Fields

| Field | Type | Description |
|---|---|---|
| `registration` | OneToOneField → Registration | One payment per registration |
| `transaction_id` | CharField | Auto-generated (`TXN-XXXXXXXXXX`) |
| `amount` | DecimalField | Copied from `event.ticket_price` at registration time |
| `payment_status` | CharField | pending / paid / failed |
| `payment_date` | DateTimeField | Auto-set on creation |

### Payment Flow (`/payments/<pk>/pay/`)

This is a **simulated payment gateway** — no real money involved.

1. User is shown a payment summary: event name, registration ID, amount, transaction ID
2. Two buttons:
   - **Simulate Successful Payment** → `payment_status = 'paid'`
   - **Simulate Failed Payment** → `payment_status = 'failed'`
3. Redirected to My Registrations after either action

### Free Events
- Payment is automatically created with `payment_status = 'paid'`
- User never sees the payment page

### Transaction ID Format
```
TXN-A3F9B2C1D4
```
Generated using Python `uuid4`, prefixed with `TXN-`.

---

## Attendance System

### Attendance Fields

| Field | Type | Description |
|---|---|---|
| `registration` | OneToOneField → Registration | One attendance record per registration |
| `attendance_status` | CharField | present / absent |
| `marked_at` | DateTimeField | Auto-updated every time saved |

### Mark Attendance (`/attendance/event/<event_pk>/mark/`)

Only the event's organizer or an Admin can mark attendance.

1. Click "Mark Attendance" on event detail page or organizer dashboard
2. Table shows all active registrations for that event
3. Each row has a dropdown: **Present** or **Absent** (pre-filled if already marked)
4. Submit saves all records using `update_or_create` — can be updated multiple times

### Attendance History (`/attendance/history/`)
- Participant sees their attendance across all registered events
- Shows: Event, Date, Attendance Status, Marked On
- "Not Marked" shown if organizer hasn't marked yet

---

## Feedback System

### Feedback Fields

| Field | Type | Description |
|---|---|---|
| `user` | ForeignKey → CustomUser | Who wrote the review |
| `event` | ForeignKey → Event | Which event |
| `rating` | IntegerField (1–5) | Star rating |
| `comment` | TextField | Optional written review |
| `created_at` | DateTimeField | Auto-set |

### Submit Feedback (`/feedback/event/<event_pk>/submit/`)

**Eligibility checks (in order):**

1. Event status must be `completed`
2. User must have an active registration for the event
3. User must have been **marked Present** in attendance — absent users cannot review
4. User must not have already submitted feedback for this event

### Where Feedback Appears
- Event Detail page shows all reviews as cards
- Average rating is shown: e.g., `★ 4.3/5 (12 reviews)`

---

## Dashboard System

The dashboard at `/dashboard/` **auto-detects the user's role** and renders the correct view.

### Admin Dashboard

| Section | Content |
|---|---|
| Stats Cards | Total Participants, Total Organizers, Total Events, Total Registrations, Total Revenue |
| Chart | Bar chart — Registrations per Event (top 8) |
| Table | Last 10 registrations system-wide |

### Organizer Dashboard

| Section | Content |
|---|---|
| Stats Cards | My Events count, Total Revenue, Total Attendance (present) |
| Charts | Bar chart — Registrations per Event + Bar chart — Revenue per Event |
| Table | All their events with Edit / Attendance / Export CSV actions |

### Participant Dashboard

| Section | Content |
|---|---|
| Stats Cards | Registered Events, Present Count, Absent Count |
| Chart | Pie chart — Attendance Summary (Present vs Absent %) |
| Lists | My Registrations + Recent Payments |

### How Charts Work

Charts are generated server-side with Matplotlib and embedded directly in HTML:

1. Data fetched from the database
2. Matplotlib renders the chart to a `BytesIO` buffer
3. Buffer is base64-encoded to a string
4. Passed to template as context variable
5. Displayed as `<img src="data:image/png;base64,{{ chart }}">`
6. No chart file is saved to disk

---

## Search & Filter

Available on the Browse Events page (`/events/`):

| Filter | Mechanism |
|---|---|
| Search by title/description | `Q(title__icontains=q) OR Q(description__icontains=q)` |
| Category | Filters `event.category_id` |
| Price | Free = `ticket_price=0`, Paid = `ticket_price > 0` |
| Status | Filters `event.status` |

All filters chain together as AND conditions. Result count shown above the grid.

Example URL:
```
/events/?q=python&category=1&price=paid&status=upcoming
```

---

## CSV Export

**URL:** `/events/<pk>/export/`  
**Access:** Event's organizer or Admin only

**Exported columns:**

| Column | Description |
|---|---|
| Registration ID | e.g., `REG-A3F9B2C1` |
| User | Username |
| Email | User's email |
| Registered At | Formatted date |
| Status | active / cancelled |
| Payment Status | pending / paid / failed / N/A |

Triggers a file download in the browser. No file is saved on the server.

---

## Email Notifications

**When sent:** Automatically after a successful event registration.

**Email content:**
- Subject: `Registration Confirmed: {event title}`
- Body: Username, event title, registration ID, date, time, venue

**Configuration in `settings.py`:**

```python
EMAIL_HOST_USER = 'YOUR_EMAIL@gmail.com'     # ← Fill this
EMAIL_HOST_PASSWORD = 'YOUR_APP_PASSWORD'    # ← Fill this (Gmail App Password)
```

> Email uses `fail_silently=True` — if credentials are missing, registration still succeeds and the app does not crash.

---

## Admin Panel

**URL:** `/admin/`  
**Access:** Superuser only (`python manage.py createsuperuser`)

| Model | List Display | Filters | Search |
|---|---|---|---|
| CustomUser | username, email, role, phone, is_active | role, is_active | — |
| Category | name | — | — |
| Event | title, organizer, category, date, status, seats, price | status, category | title, venue |
| Registration | registration_id, user, event, date, status | status | registration_id, username |
| Payment | transaction_id, registration, amount, status, date | payment_status | — |
| Attendance | registration, status, marked_at | attendance_status | — |
| Feedback | user, event, rating, created_at | rating | — |

---

## Database Models & Relationships

```
CustomUser
    │
    ├──(organizer)──► Event ◄──── Category
    │                   │
    │                   └──► Registration ◄──(user) CustomUser
    │                              │
    │                              ├──► Payment        (OneToOne)
    │                              └──► Attendance     (OneToOne)
    │
    └──(user)──► Feedback ──► Event
```

| Relationship | Type | On Delete |
|---|---|---|
| Event → CustomUser (organizer) | ForeignKey | CASCADE |
| Event → Category | ForeignKey | SET_NULL |
| Registration → CustomUser | ForeignKey | CASCADE |
| Registration → Event | ForeignKey | CASCADE |
| Payment → Registration | OneToOneField | CASCADE |
| Attendance → Registration | OneToOneField | CASCADE |
| Feedback → CustomUser | ForeignKey | CASCADE |
| Feedback → Event | ForeignKey | CASCADE |

---

## URL Structure

```
/                                      Home page
/events/                               Browse all events
/events/<pk>/                          Event detail
/events/create/                        Create event (organizer/admin)
/events/<pk>/edit/                     Edit event (organizer/admin)
/events/<pk>/delete/                   Delete event (organizer/admin)
/events/<pk>/export/                   Download registrations as CSV

/accounts/register/                    Registration page
/accounts/login/                       Login page
/accounts/logout/                      Logout
/accounts/profile/                     Edit profile

/registrations/event/<pk>/register/    Register for an event
/registrations/<pk>/cancel/            Cancel a registration
/registrations/my/                     View my registrations

/payments/<pk>/pay/                    Simulated payment page
/payments/history/                     Payment history

/attendance/event/<pk>/mark/           Mark attendance (organizer/admin)
/attendance/history/                   View attendance history (participant)

/feedback/event/<pk>/submit/           Submit feedback for a completed event

/dashboard/                            Role-based dashboard (auto-detected)

/admin/                                Django admin panel
```

---

## Sample Data

Run `python manage.py seed_data` to load:

### Users

| Username | Password | Role |
|---|---|---|
| `organizer1` | `organizer123` | Organizer |
| `user1` | `user12345` | Participant |

### Categories
`Technology` · `Music` · `Sports` · `Workshop` · `Conference` · `Art`

### Events (created by organizer1)

| Title | Price | Seats | Status |
|---|---|---|---|
| Python Workshop 2025 | ₹500 | 50 | Upcoming |
| Web Dev Bootcamp | ₹1200 | 30 | Upcoming |
| Free Music Festival | Free | 200 | Upcoming |

---

## Key Validations

| Rule | Where Enforced |
|---|---|
| Event date cannot be in the past | `EventForm.clean_date()` |
| Total seats must be > 0 | `EventForm.clean()` |
| No duplicate registrations | DB `unique_together` + view check |
| Cannot register for a full event | `event.is_full()` check in view |
| Cannot register for cancelled/completed events | Status check in view |
| Only organizer can edit/delete their own events | `event.organizer == request.user` check |
| Only attendees marked Present can leave feedback | Attendance query in feedback view |
| Feedback only for completed events | `event.status == 'completed'` check |
| One feedback per user per event | DB `unique_together` + view check |
| All protected views require login | `@login_required` decorator |
| All forms protected against CSRF | `{% csrf_token %}` in every form |

---

## Apps Summary

| App | Responsibility |
|---|---|
| `accounts` | CustomUser model, registration, login, logout, profile |
| `events` | Event & Category models, CRUD, search/filter, CSV export |
| `registrations` | Registration model, register/cancel flow |
| `payments` | Payment model, simulated payment gateway |
| `attendance` | Attendance model, mark and view attendance |
| `feedback` | Feedback model, star ratings for completed events |
| `dashboard` | Role-based dashboards with Matplotlib charts |

---

*Built as a PFSD Academic Project — Django 6.0.4 · SQLite · Bootstrap 5*
