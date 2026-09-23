# 💰 Personal Finance Advisor Bot

An AI-powered personal finance management web application built with **Flask**, **SQLAlchemy**, **SQLite**, **Bootstrap 5**, and **Generative AI** (Groq/Gemini).

## ✨ Features
- 🔐 **Secure User Authentication**: Registration, Login, Logout with password hashing (Bcrypt) and session management (Flask-Login).
- 📊 **Financial Dashboard**: Real-time summaries of Total Income, Total Expenses, and Net Balance in Indian Rupees (₹).
- 💳 **Transaction Tracking**: Log, categorize, and review financial transactions.
- 🤖 **AI Financial Advisor**: Generates spending analysis, overspending alerts, personalized 50/30/20 budget allocations, and savings recommendations via Generative AI LLM.
- 📱 **Mobile Teleprompter**: Built-in `/script` route optimized for mobile video presentations and walkthroughs.
- 🌐 **Public Deployment Ready**: Compatible with Ngrok for public tunneling and demonstrations.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Flask-Login, Flask-Bcrypt
- **Database:** SQLAlchemy ORM, SQLite
- **Frontend:** Jinja2, Bootstrap 5, Marked.js
- **AI Engine:** Generative AI API (Groq/Gemini)
- **Deployment:** Ngrok

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Whitedevil964/Personal-Finance-Advisor-Bot.git
cd Personal-Finance-Advisor-Bot
```

### 2. Set up virtual environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file from `.env.example`:
```env
FLASK_APP=run.py
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///finance.db
GEMINI_API_KEY=your_ai_api_key_here
```

### 5. Run the Application
```bash
python run.py
```
Visit `http://127.0.0.1:5000` in your browser.

