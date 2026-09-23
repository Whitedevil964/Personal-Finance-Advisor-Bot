from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Transaction, Budget

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Calculate summary data
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense
    
    # Get latest budget
    latest_budget = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.year.desc(), Budget.month.desc()).first()
    
    return render_template('dashboard/index.html', 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           balance=balance,
                           latest_budget=latest_budget,
                           recent_transactions=transactions[-5:])

@dashboard_bp.route('/script')
def presentation_script():
    return render_template('script.html')

