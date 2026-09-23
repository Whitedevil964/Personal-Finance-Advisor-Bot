import os
import requests
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Transaction

advisor_bp = Blueprint('advisor', __name__)

def generate_financial_advice(income, expenses, categories):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    if not api_key or api_key == "your_gemini_api_key_here":
        return "Please configure your GEMINI_API_KEY in the .env file to see AI insights."
    
    category_summary = "\n".join([f"- {k}: ₹{v:.2f}" for k, v in categories.items()]) if categories else "No categorized expenses recorded yet."
    
    prompt = f"""You are an expert Personal Finance Advisor Bot.
Analyze the following financial data and provide personalized budget generation, spending analysis, and actionable savings recommendations. All amounts are in Indian Rupees (INR, ₹).

Financial Data:
- Total Income: ₹{income:.2f}
- Total Expenses: ₹{expenses:.2f}
- Net Savings/Balance: ₹{(income - expenses):.2f}
- Expense Breakdown by Category:
{category_summary}

Please provide a structured, easy-to-read response with the following sections (always quote monetary figures in Indian Rupees '₹'):
1. 📊 Spending Analysis & Financial Health
2. ⚠️ Overspending & Budget Alerts (if any)
3. 💡 Cost Optimization Suggestions
4. 🎯 Recommended Monthly Budget Allocation (Needs / Wants / Savings)
5. 🚀 Actionable Steps to Improve Savings
"""

    try:
        # Check for Groq API key (starts with gsk_)
        if api_key.startswith("gsk_"):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {"role": "system", "content": "You are a professional financial advisor."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                result = resp.json()
                return result["choices"][0]["message"]["content"]
            else:
                # Fallback to qwen model if gpt-oss is busy/unavailable
                payload["model"] = "qwen/qwen3.8-27b"
                resp = requests.post(url, headers=headers, json=payload, timeout=20)
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
                return f"Groq API Error ({resp.status_code}): {resp.text}"

        # Otherwise, handle as Gemini API key
        else:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ]
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                result = resp.json()
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "No response generated.")
                return "Received empty response from Gemini API."
            else:
                return f"Gemini API Error ({resp.status_code}): {resp.text}"

    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"

@advisor_bp.route('/advisor')
@login_required
def insights():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    
    categories = {}
    for t in transactions:
        if t.type == 'expense':
            categories[t.category] = categories.get(t.category, 0) + t.amount
            
    advice = generate_financial_advice(total_income, total_expense, categories)
    
    return render_template('advisor/insights.html', advice=advice, total_income=total_income, total_expense=total_expense)
