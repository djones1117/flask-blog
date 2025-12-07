# Personal Blog (Flask + AWS S3)

A lightweight full-stack blog application built with Flask that supports user authentication, CRUD posts, and image uploads to AWS S3. Designed as a clean, production-style portfolio app with environment-based configuration and simple deployment using Gunicorn on Render.

## Live Demo
**Deployed URL:** https://flask-personal-blog-32q0.onrender.com

> Free Render instances may sleep with inactivity, so the first load can be slow.

---

## Features
- User registration + login/logout
- Create, edit, delete posts
- Upload an image per post
- Images stored in AWS S3 
- Clean post card layout with controlled image sizing
- Secure filename handling + UUID-based S3 object keys

---

## Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **Database:** SQLite
- **Storage:** AWS S3
- **Frontend:** Jinja2 + CSS
- **Deployment:** Render

---

## Local Setup

### 1 Clone + virtual env
    git clone https://github.com/djones1117/flask-blog.git
    cd flask-blog
    python3 -m venv venv
    source venv/bin/activate

### 2 Install dependencies
    pip install -r requirements.txt

### 3 Environment variables
Create a `.env` file (do not commit this):

   

### 4 Initialize DB
    flask --app flaskr init-db

### 5 Run locally
    flask --app flaskr run --debug

Open:
- http://127.0.0.1:5000/

---

## AWS S3 Upload Notes
Uploads are handled through:
- Secure filenames (`secure_filename`)
- Unique object keys (`uuid4`)
- Content-type preserved for correct browser rendering

Bucket settings should allow public read access for uploaded objects (via bucket policy).  
This project avoids ACL usage to remain compatible with buckets that disable ACLs.

---

## Deployment (Render)

### Build Command
    pip install -r requirements.txt

### Start Command
    gunicorn "flaskr:create_app()"

### Required Render Environment Variables
Set these in Render → Environment:
- `SECRET_KEY`
- `S3_BUCKET_NAME`
- `AWS_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Initialize DB on Render
After the service is created, open Render Shell/Console and run:

    flask --app flaskr init-db

---




## What This Project Demonstrates
- Flask app factory pattern
- Auth + protected routes
- Clean database interactions
- Production-style env config
- Real cloud integration (AWS S3)
- Deployment with Gunicorn

---


