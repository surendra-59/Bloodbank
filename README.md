# BLOODBANK
🩸 Blood Bank Management System (BBMS)
A role-based web application that digitizes and automates blood bank operations — from donor management to blood inventory and hospital requests.

✅ Use Case
Improve emergency response time during blood shortages

Reduce human error in donor eligibility and stock management

Digitally connect donors, hospitals, and blood bank admins in a single platform

Enable real-time blood request and allocation workflows

Support health campaigns and awareness via blog/social modules

⚙️ Tools & Technologies
Purpose	Tech Stack
Backend	Python, Django
Frontend	HTML, CSS, JavaScript, Bootstrap
Database	MySQL
DevTools	VS Code, Git, GitHub
Server (Local)	Django Dev Server / XAMPP
Others	Excalidraw, Draw.io

🔐 Roles & Features
🔑 Admin
Approve or reject hospital & donor registrations

Handle blood requests & donor responses

Manage blood inventory

Send alerts to eligible donors

Access blog dashboard and system logs

🏥 Hospital
Register/login and request specific blood types

Track request status and receive notifications

🧑‍🦰 Donor
Register/login, view and accept/reject requests

Enter height & weight for BMI check

View donation history and profile

🧩 Key Modules
Role-Based User Management

BMI-Based Donor Eligibility Check

Blood Inventory Management

Donor Notification System

Hospital Request Workflow

Blog Module (Post, Like, Comment)

Password Reset via Email

Secure Authentication & Session Handling

🚀 Setup Instructions
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/Surendra-58/bloodbank2.git
cd bloodbank2

# 2. Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
📷 Screenshots (Optional)
Add actual UI screenshots here if available:

Admin Dashboard

Donor BMI Validation

Hospital Blood Request Form

Blog Page

📬 Contact / Contribute
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

GitHub: Surendra-59/bloodbank
