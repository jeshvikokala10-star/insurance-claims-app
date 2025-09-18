
🛡️ Insurance Claims Processing App

This project is a Flask + SQLite web app for managing insurance claims.
It is fully Dockerized so you can run it easily.

📂 1. Project Directory Structure

insurance-claims-app/
│── app.py              # Main Flask backend
│── requirements.txt    # Dependencies (Flask, gunicorn)
│── Dockerfile          # Docker instructions
│── templates/
│    └── claim_form.html
│── static/
│    └── style.css


💻 2. Create the Project Folders

Open Command Prompt (Windows) or Terminal (Linux/Mac):

mkdir insurance-claims-app
cd insurance-claims-app

mkdir templates
mkdir static


📝 3. Add Files

Inside insurance-claims-app/ create these files:

app.py → Flask backend

requirements.txt → Python dependencies

Dockerfile → Docker setup


Inside templates/ create:

claim_form.html


Inside static/ create:

style.css


✅ Important: Make sure file extensions are correct (.py, .html, .css, .txt, no hidden .txt.txt).


🐍 4. (Optional) Test Locally

If you want to run without Docker first:

pip install -r requirements.txt
python app.py

Open 👉 http://localhost:5000

🐳 5. Run with Docker

Step 1: Build Docker Image

docker build -t insurance-claims-app .

Step 2: Run Docker Container

docker run -d -p 5009:5000 --name insurance-claims-app insurance-claims-app

5009:5000 → maps local port 5009 to container’s port 5000

Open 👉 http://localhost:5009


Step 3: Check Logs (if needed)

docker logs insurance-claims-app

Step 4: Stop & Remove Container (when needed)

docker stop insurance-claims-app
docker rm insurance-claims-app


✅ Features

📄 Claim submission form

📂 Document upload (/uploads/)

🗄️ SQLite database (/data/claims.db)

⚡ Simple AI rules:

≤ 1000 → Approved

> 50,000 → Escalated

Contains “fraud/fake” → Rejected
