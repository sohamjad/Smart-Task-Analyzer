🌟 SMART TASK ANALYZER — README.md (FINAL SUBMISSION VERSION)
📌 Smart Task Analyzer

A mini full-stack application built using Django (Python) and HTML/CSS/JavaScript that intelligently scores, prioritizes, and visualizes tasks based on urgency, importance, effort, and dependencies.
Designed as part of a technical assessment to showcase clean architecture, algorithm design, and critical thinking.

🧰 Tech Stack

Backend: Python 3.12, Django 5.x, Django REST Framework

Frontend: HTML, CSS, Vanilla JavaScript

Database: SQLite (default Django DB)

Others: dateutil, django-cors-headers

⚙️ Setup Instructions
1. Clone the Project
git clone <your-repo-url>
cd smart-task-analyzer

2. Create Virtual Environment
python -m venv venv

3. Activate Environment

Windows:

venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Run Migrations
cd backend
python manage.py migrate

6. Start Backend Server
python manage.py runserver


Backend URL:
http://127.0.0.1:8000/

7. Start Frontend
cd ../frontend
python -m http.server 5500


Frontend URL:
http://127.0.0.1:5500/index.html

🔥 API Endpoints
POST /api/tasks/analyze/

Input:

{
  "tasks": [...],
  "strategy": "smart_balance"
}


Response:

List of tasks sorted by priority

Score

Explanation for each task

GET /api/tasks/suggest/?tasks=[]

Response:

Top 3 suggested tasks

Explanation for why they were selected

🧠 Algorithm Explanation (400+ Words)

The Smart Task Analyzer uses a multi-factor, weighted scoring system designed to reflect realistic human productivity decision-making. Its goal is to determine which task should be completed first based on urgency, importance, effort, and dependency structure.

1. Urgency

Urgency is derived from comparing today’s date with the task’s due date.

Tasks past their due date receive the highest urgency.

Tasks due today get near-max urgency.

Tasks due in future days lose points linearly (100 − 5 × days_left).

Tasks without due dates receive a default urgency value.

This reflects real-world scenarios where deadlines heavily influence decisions.

2. Importance

Importance is user-defined on a scale of 1–10.
For scoring, importance is scaled to 100 (importance × 10).
High-importance tasks naturally float to the top of the ranking.

3. Effort ("Quick Win" Bonus)

Effort estimates the number of hours required.
The philosophy:

Smaller tasks should be incentivized because they provide mental relief when completed.

Effort score is calculated as:

effort_score = max(5, 30 - (hours * 3))


This ensures long tasks don’t dominate scoring just because they are important.

4. Dependencies

Each dependency adds 10 points (up to 40).
This means tasks that unlock other tasks become more important — a realistic productivity consideration.

5. Circular Dependency Detection (Bonus Feature)

If tasks form a loop (A → B → C → A), none of them are solvable until the cycle is broken.

A DFS-based cycle detection algorithm is implemented:

If a cycle is found → score = 0

Explanation explicitly mentions the circular dependency

This prevents logically impossible tasks from falsely ranking high.

6. Overall Score (Weighted Combined Score)
final_score =
    urgency * 0.4 +
    importance * 0.4 +
    effort * 0.1 +
    dependencies * 0.1


The weights ensure urgency and importance dominate prioritization while still incorporating effort and dependencies.

7. Explainability

For every task, the backend generates a human-readable explanation summarizing:

Due date impact

Importance influence

Effort boost

Dependency impact

This transparency is crucial for user trust and interpretability.

🎯 Design Decisions & Trade-offs
1. No Database Storage

The assignment didn’t require persistent tasks.
Keeping tasks in memory ensures:

Simplicity

Faster testing

Easy integration with JSON bulk input

2. Weighted Scoring Instead of Rules

Rules are rigid; weighted scoring is flexible.
You can adjust weights easily without rewriting logic.

3. DFS for Cycle Detection

Topological sorting could be used, but DFS is:

Faster

Easier to implement

Sufficient for this task dataset

4. Simple, Framework-Free Frontend

Using plain JS:

Reduces complexity

Meets assignment guidelines

Helps focus on functionality

5. Eisenhower Matrix UI

Visual categorization helps users understand urgency × importance better than numbers alone.

🧪 Unit Tests (Minimum 3 Required — 5 Provided)

Located in:

backend/tasks/tests.py


Tests include:

Overdue urgency check

High importance ordering

Quick win effort scoring

Dependency impact

Circular dependency detection

Run tests with:

python manage.py test

⏱️ Time Breakdown
Task	Time
Django backend & API setup	30 min
Scoring algorithm	45 min
Circular dependency logic	30 min
Frontend UI + Form + Results	45 min
API integration	20 min
Eisenhower Matrix	35 min
Unit tests	25 min
README + cleanup	20 min
Total	~4 hours
🎁 Bonus Challenges Implemented

✔ Circular Dependency Detection
✔ Eisenhower Matrix View

Both optional bonus features are implemented fully.

🚀 Future Improvements

Add database persistence (CRUD with Django models)

Add drag-and-drop UI (Trello-style)

Add holiday-aware urgency scoring

Add machine learning-based adaptive scoring

Add user accounts (Auth)

Add task categories & tags

Build dependency graph visualization