from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Transaction

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/transactions')
@login_required
def transactions():
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('finance/transactions.html', transactions=user_transactions)

@finance_bp.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        type = request.form.get('type')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description')
        
        transaction = Transaction(
            user_id=current_user.id,
            type=type,
            amount=amount,
            category=category,
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('finance.transactions'))
        
    return render_template('finance/add_transaction.html')

