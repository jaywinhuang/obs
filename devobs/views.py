from flask import render_template, request, jsonify, redirect, g, url_for
from flask_login import login_user, login_required, current_user, logout_user
from devobs import app, db, lm
from .models import Users, Transaction, Account, Bill, Transfer, Deposit
import traceback
import time
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/account-activity')
@login_required
def balance():
    return render_template('account-activity.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/transfer')
@login_required
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
        print g.user.get_id()
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
        "message": "success",
        "data": []
    }

    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username, password=password).first()
        if user is not None:
            login_user(user)
        else:
            result['status'] = 2
            result['message'] = "user name or password incorrect"
    except Exception, e:
        result['status'] = 1
        result['message'] = "Login error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route('/api/user/accounts', methods=['GET'])
@login_required
def get_accounts():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }

    accounts = g.user.accounts
    for acnt in accounts:
        tmp = {
            "accountNumber": acnt.account_num,
            "type": acnt.type,
            "balance": acnt.balance
        }
        result['data'].append(tmp)

    return jsonify(result)

@app.route('/api/user/transactions', methods=['POST'])
@login_required
def get_transactions():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }

    try:
        account_num1 = request.form.get('accountNumber')
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
        result['message'] = "Get transaction error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route('/api/user/transfer', methods=['POST'])
def transfer_funds():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        fromacnt = request.form.get('fromAccount')
        toacnt = request.form.get('toAccount')
        amt = float(request.form.get('amount'))
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')

        from_account = g.user.accounts.filter(Account.account_num == fromacnt).first()
        to_account = g.user.accounts.filter(Account.account_num == toacnt).first()

        if from_account is not None and to_account is not None:
            if from_account.balance - amt >= 0:
                from_account.balance -= amt
                to_account.balance += amt

                # insert transfer record
                transf = Transfer(from_account=fromacnt, to_account=toacnt, amount=amt, time=curr_time)
                db.session.add(transf)
                db.session.commit()
                transf_id = transf.transfer_id

                # insert transaction history record
                transaction_from = Transaction(account_num=fromacnt, amount=-amt, type='transfer', time=curr_time,
                                          remark='transfer to '+toacnt, operation_id=transf_id)
                transaction_to = Transaction(account_num=toacnt, amount=amt, type='transfer', time=curr_time,
                                          remark='transfer from '+fromacnt, operation_id=transf_id)
                db.session.add(transaction_from)
                db.session.add(transaction_to)
                db.session.commit()

            else:
                result['status'] = 2
                result['message'] = "Insufficient funds in from account"
        else:
            result['status'] = 3
            result['message'] = "Cannot find account"
    except Exception, e:
        result['status'] = 1
        result['message'] = "Transfer error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route('/api/user/deposit', methods=['POST'])
def deposit_by_check():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        to_account = request.form.get('toAccount')
        amount = int(request.form.get('amount'))
        check_number = request.form.get('checkNumber')
        memo = request.form.get('memo')
        check_image_front = request.files['checkImageFront']
        check_image_back = request.files['checkImageBack']
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')

        check_info = Deposit.query.filter_by(account_num=to_account, check_num=check_number, amount=amount).first()
        if check_info is not None:
            front_image_path = base_dir+"/checkImage/" + check_number +"-front.jpg"
            check_image_front.save(front_image_path)
            back_image_path =  base_dir+"/checkImage/" + check_number +"-back.jpg"
            check_image_back.save(back_image_path)
            check_info.img_path = front_image_path + ":" + back_image_path
            to_account_info = Account.query.filter_by(account_num=to_account).first()
            to_account_info.balance += amount

            transaction_info = Transaction(account_num=to_account, amount=amount, type="deposit by check", time=curr_time,
                    remark="deposit by check:" + check_number, operation_id=check_info.deposit_id)
            db.session.add(transaction_info)
            db.session.commit()
        else:
            result['status'] = 2
            result['message'] = "Check info is not right"
            return jsonify(result)

    except Exception, e:
        result['status'] = 1
        result['message'] = ""
        print traceback.format_exc()

    return jsonify(result)

@app.route("/api/user/profile", methods=['GET', 'POST'])
def user_profile():
    result = {
        "status": 0,
        "message": "success",
        "data": {}
    }

    if request.method == 'GET':
        # TODO your code
        pass

    if request.method == 'POST':
        # TODO
        pass

    return jsonify(result)

@app.route("/api/user/paybill", methods=['POST'])
def pay_bill():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        from_account = request.form.get("fromAccount")
        amount = int(request.form.get("amount"))
        biller_name = request.form.get("billerName")
        biller_account = request.form.get("billerAccount")
        biller_address = request.form.get("billerAddress")
        biller_city = request.form.get("billerCity")
        biller_state = request.form.get("billerState")
        biller_zip = request.form.get("billerZip")
        biller_phone = request.form.get("billerPhone")
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')

        bill_info = Bill(from_account=from_account, amount=amount, time=curr_time,
            biller_name=biller_name, biller_account=biller_account, biller_address=biller_address, biller_state=biller_state,
            biller_city=biller_city, biller_zip=biller_zip, biller_phone=biller_phone)
        # should first add bill and commit, then it can generate the bill id
        db.session.add(bill_info)
        db.session.commit()
        if bill_info is not None:
            from_account_info = Account.query.filter_by(account_num=from_account).first()
            to_account_info = Account.query.filter_by(account_num=biller_account).first()
            if from_account_info is not None and to_account_info is not None:
                if from_account_info.balance > amount:
                    from_account_info.balance -= amount
                    to_account_info.balance += amount
                else:
                    result['status'] = 2
                    result['message'] = "The account's balance is not enough"
                    return jsonify(result)
            else:
                result['status'] = 3
                result['message'] = "The account info is error"
                return jsonify(result)

        transaction_info = Transaction(account_num=from_account, amount=amount, type="pay bill", time=curr_time,
                        remark="pay bill to:"+biller_account, operation_id=bill_info.bill_id)

        db.session.add(transaction_info)
        db.session.commit()

    except Exception, e:
        result['status'] = 1
        result['message'] = ""
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route("/api/user/enroll/check", methods=['POST'])
def check_enroll():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        ssn = request.form.get("ssn")
        pin = request.form.get("pin")
        any_account = request.form.get("anyAccount")
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # TODO check the logic
        user_info = Users.query.filter_by(ssn=ssn, pin=pin).first()
        if user_info is not None:
            account_info = Account(account_num=any_account, user_id=user_info.user_id, balance=0, type="", created_time=curr_time)
            db.session.add(account_info)

        else:
            result['status'] = 2
            result['message'] = "The ssn or pin is error"
            return jsonify(result)

        db.session.commit()

    except Exception, e:
        result['status'] = 1
        result['message'] = ""
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@app.route("/api/user/enroll/update", methods=['POST'])
def update_enroll_info():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        security_question = request.form.get("securityQuestion")
        security_answer = request.form.get("securityAnswer")
        # TODO check the logic
        user_info = Users.query.filter_by(username=username).first()
        if user_info is not None:
            user_info.username = username
            user_info.password = password
            user_info.first_name = firstname
            user_info.last_name = lastname
            user_info.email = email
            user_info.phone = phone
            user_info.address = address
            user_info.security_question = security_question
            user_info.security_answer = security_answer
        else:
            result['status'] = 2
            result['message'] = "The user has not been enrolled"
            return jsonify(result)

        db.session.commit()

    except Exception, e:
        result['status'] = 1
        result['message'] = ""
        app.logger.error(traceback.format_exc())

    return jsonify(result)
