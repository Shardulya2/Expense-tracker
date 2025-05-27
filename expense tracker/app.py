from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from io import BytesIO
from io import StringIO
from datetime import datetime
from calendar import monthrange
import csv
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------- Database Setup ----------

def init_db():
    with sqlite3.connect("expense.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount REAL,
                            category TEXT,
                            date TEXT,
                            note TEXT
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT
                        )''')
        conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin')")

# Call once at startup
init_db()

def get_db_connection():
    conn = sqlite3.connect("expense.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Constants ----------
MONTHLY_LIMIT = 1000

# ---------- Routes ----------

@app.route('/')
def index():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    conn = get_db_connection()
    cursor = conn.execute(query, params)
    expenses = [dict(row) for row in cursor.fetchall()]

    today = datetime.today()
    start_month = today.replace(day=1).strftime('%Y-%m-%d')
    end_month = today.replace(day=monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')

    monthly_total = conn.execute(
        "SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?",
        (start_month, end_month)
    ).fetchone()[0] or 0

    conn.close()
    return render_template(
        "index.html",
        expenses=expenses,
        start_date=start_date,
        end_date=end_date,
        monthly_total=monthly_total,
        limit=MONTHLY_LIMIT
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        note = request.form["description"]
        amount = float(request.form["amount"])
        
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (date, category, note, amount) VALUES (?, ?, ?, ?)",
            (date, category, note, amount)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    
    return render_template("add_edit.html", expense=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        note = request.form['description']

        conn.execute("UPDATE expenses SET amount=?, category=?, date=?, note=? WHERE id=?",
                     (amount, category, date, note, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        expense = conn.execute("SELECT * FROM expenses WHERE id=?", (id,)).fetchone()
        conn.close()
        return render_template("add_edit.html", expense=expense)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/report')
def report():
    conn = get_db_connection()
    data = conn.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category").fetchall()
    conn.close()
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("report.html", labels=labels, values=values)

@app.route('/download-pdf')
def download_pdf():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Expenses Report", ln=True, align="C")
    pdf.ln(10)

    for e in expenses:
        pdf.cell(200, 10, txt=f"Date: {e['date']} | Category: {e['category']} | Note: {e['note']} | Amount: ${e['amount']}", ln=True)

    # Write the PDF into a BytesIO buffer correctly
    output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Generate PDF as a string, then encode
    output.write(pdf_bytes)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="expenses.pdf", mimetype='application/pdf')


@app.route('/download-csv')
def download_csv():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    # Use StringIO to write CSV as text
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Note'])
    for row in expenses:
        writer.writerow([row['id'], row['amount'], row['category'], row['date'], row['note']])

    # Convert the StringIO text to bytes for sending as a file
    output = BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='expenses.csv', mimetype='text/csv')

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
