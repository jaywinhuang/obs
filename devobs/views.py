from flask import render_template, request, jsonify, redirect, g, url_for
from flask_login import login_user, login_required, current_user, logout_user
from devobs import app, db, lm
from .models import Users, Transaction, Account, Bill, Transfer, Deposit
import traceback


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/account-activity')
def balance():
    return render_template('account-activity.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/billpay')
def billpay():
    return render_template('billpay.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect((url_for('index')))
    else:
        return render_template('login.html')

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.before_request
def befor_reques():
    g.user = current_user


#############################
# Here is the ajax request
#############################

@app.route('/api/user/login', methods=['POST'])
def login_auth():
    result = {
        "status": 0,
        "msg": "success",
        "data": {}
    }

    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username, password=password).first()
        if user is not None:
            login_user(user)
        else:
            result['status'] = 2
            result['msg'] = "user name or password incorrect"
    except Exception, e:
        result['status'] = 1
        result['msg'] = "Login error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route('/api/user/accounts', methods=['GET'])
@login_required
def get_accounts():
    result = {
        "status": 0,
        "msg": "success",
        "data": []
    }

    accounts = g.user.accounts
    for acnt in accounts:
        tmp = {
            "account_num": acnt.account_num,
            "type": acnt.type,
            "balance": acnt.balance
        }
        result['data'].append(tmp)

    return jsonify(result)

@app.route('/api/account/transactions', methods=['POST'])
@login_required
def get_transactions():
    result = {
        "status": 0,
        "msg": "success",
        "data": []
    }

    try:
        account_num1 = request.form.get('account_num')
        transactions = db.session.query(Transaction).filter(Transaction.account_num == account_num1)
        for trans in transactions:
            tmp = {
                "dateTime": trans.time,
                "type": trans.type,
                "desc": trans.remark,
                "amount": trans.amount
            }
            result['data'].append(tmp)

    except Exception, e:
        result['status'] = 1
        result['msg'] = "Get transaction error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route('/api/user/transfer', methods=['POST'])
def transfer():
    result = {
        "status": 0,
        "msg": "success",
        "data": []
    }
    try:
        fromacnt = request.form.get('from_account')
        toacnt = request.form.get('to_account')
        amt = request.form.get('amount')
        # from_account = Account.query.join(Users, Users.user_id == Account.user_id)\
        #     .filter(Users.user_id == g.user.user_id).filter_by(Account.account_num == )
        from_account = g.user.accounts.filter_by(Account.account_num == fromacnt)
        to_account = g.user.accounts.filter_by(Account.account_num == toacnt)
        if from_account is not None and to_account is not None:
            if from_account.balance - amt >= 0:
                from_account.balance -= amt
                to_account.balance += amt
            else:
                result['status'] = 2
                result['msg'] = "Insufficient funds in from account"
        else:
            result['status'] = 3
            result['msg'] = "Cannot find account"
    except Exception, e:
        result['status'] = 1
        result['msg'] = "Transfer error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)