# Inform-agency
### Database Structure:
- inform_agency![diagram_db_structure_inform_agency.png](diagram_db_structure_inform_agency.png)

## Project description 
  ***Inform-agency*** - is a web-based application for managing news, editors and topics.  
Users can create, edit, and view newspapers, edit editor profiles, and search for news by topic.

___

## 🚀 Functionality

- Registration and authentication of editors (redactors)
- Newspaper management (CRUD: create, edit, review, delete)
- Manage editors (redactors)
-  Search for news by topic
- Bootstrap 5 for UI

---

## 📦 Installation

### 1️⃣ **Clone the repository**. 
https://github.com/andreykolomiec/Inform-agency.git

### 2️⃣ Create a virtual environment and activate it
python -m venv venv
- Windows:
  - venv\Scripts\activate

- Mac/Linux:
  - source venv/bin/activate

### 3️⃣ Setting up dependencies
pip install -r requirements.txt

### 4️⃣ Setting up the database and applying migrations
python manage.py migrate

### 5️⃣ Create a superuser (for access to the admin panel)
python manage.py createsuperuser

### 6️⃣ Starting the server
python manage.py runserver

### The application will be available at: http://127.0.0.1:8000/
### To access the page after registration: http://127.0.0.1:8000/newspapers/

---
### 🔧 Technology:
- Python 3.x
- Django
- PostgreSQL (або SQLite)
- Bootstrap 5
- FontAwesome
---

### 🔑 Test user:
### To test the functionality, you can use the following credentials:
- 👤 Login: user  
- 🔑 Password: user12345 
___

### Project deployment:
- 🌍 **Long version**: [Go to site] (https://inform-agency-zrtd.onrender.com/)

### 👥 Authors:
- 📂 andreykolomiec (https://github.com/andreykolomiec/Inform-agency/)


