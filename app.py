import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

UPLOAD_FOLDER = 'uploads'
DB_PATH = 'data/claims.db'
ALLOWED_EXTENSIONS = {'pdf','png','jpg','jpeg','doc','docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_number TEXT,
            claim_type TEXT,
            amount REAL,
            description TEXT,
            document TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ai_decision(claim_amount, description):
    try:
        amount = float(claim_amount)
    except:
        return 'escalated'
    desc = (description or '').lower()
    if 'fraud' in desc or 'fake' in desc:
        return 'rejected'
    if amount <= 1000:
        return 'approved'
    if amount > 50000:
        return 'escalated'
    return 'escalated'

@app.route('/')
def index():
    return render_template('claim_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    policy = request.form.get('policy_number', '').strip()
    ctype = request.form.get('claim_type', '')
    amount = request.form.get('claim_amount', '')
    description = request.form.get('description', '')

    file = request.files.get('document')
    filename_saved = None
    if file and file.filename and allowed_file(file.filename):
        fname = file.filename
        filename_saved = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{fname}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_saved))

    status = ai_decision(amount, description)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    c.execute('''
        INSERT INTO claims (policy_number, claim_type, amount, description, document, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (policy, ctype, float(amount) if amount else None, description, filename_saved, status, now))
    conn.commit()
    conn.close()

    return f"Claim submitted. Status: {status}"

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)