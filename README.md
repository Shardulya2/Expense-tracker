Expense Manager (Flask + SQLite)
======================================

A full-stack web application that allows users to track daily expenses with the ability to:
- Add, edit, delete expenses
- View interactive charts
- Filter by date
- Export as CSV or PDF
- Get notified when monthly budget is exceeded

Project Structure
-----------------
expense_manager

    app.py
 
    expense.db
 
    static
 
        css
           styles.css
        js
          chart.js
    templates

        base.html
        index.html
        add_edit.html
        report.html

Features
--------
Expense Management
- Add new expense with amount, category, date, and note
- Edit and delete existing expenses

Date Filters
- Filter expenses by start and end dates

Reports & Charts
- View category-wise bar chart for your expenses using Chart.js

Export Options
- Export all data as CSV
- Download PDF report

Budget Alerts
- Displays warning when monthly limit (e.g., ₹1000) is exceeded

Setup Instructions
------------------
1. Clone the Repo
   git clone https://github.com/your-username/daily-expense-manager.git
   cd daily-expense-manager

2. Create a Virtual Environment (optional)
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate

3. Install Dependencies
   pip install flask fpdf

4. Run the App
   python app.py

5. Visit in Browser
   http://127.0.0.1:5000/

Code Highlights
---------------
app.py
- Initializes DB with init_db()
- Handles all routes:
  - '/' - home with filters
  - '/add' - add new expense
  - '/edit/<id>' - edit expense
  - '/delete/<id>' - delete expense
  - '/report' - view chart
  - '/download-pdf' - export as PDF
  - '/download-csv' - export as CSV

templates/
- base.html – common layout for all pages
- index.html – dashboard + filters + table
- add_edit.html – form for adding/editing expenses
- report.html – bar chart using Chart.js

chart.js
- Contains Chart.js rendering logic (can be inlined in report.html too)

Future Enhancements
-------------------
- Add user login with Flask-Login
- Make it PWA/mobile-friendly
- Add daily/weekly/monthly summary widgets
- Pie chart and line graph options

Screenshots
-------------------

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/719d17f5-aac6-4976-9fec-948bd9bb64bb" />

<img width="1279" alt="image" src="https://github.com/user-attachments/assets/9c35bfd4-127c-46fe-af1e-889794801fcc" />

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/e83085d7-6889-4ceb-99d0-c670d4a08b14" />

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/aa09fa18-8a3f-4a0e-a9b3-2dc019166eb4" />




