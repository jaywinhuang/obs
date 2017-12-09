import os
import time
import traceback

from flask import request, jsonify, g, Blueprint
from flask_login import login_user, login_required
from sqlalchemy import desc

from devobs import db, app, utils
from .models import Users, Transaction, Account, Bill, Transfer, Deposit

base_dir = os.path.abspath(os.path.dirname(__file__))
apis = Blueprint("apis", __name__)


@apis.route('/')
def apis_index():
    return "I am api's index."


#############################
# Here is the ajax request
#############################

@apis.route('/user/login', methods=['POST'])
def login_auth():
    result = {
        "status": 0,
        "message": "success",
        "data": {}
    }

    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if (username is None) or (password is None):
            raise Exception
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


# @apis.route('/user/login_after_check', methods=['POST'])
# def login_after_check():
#     result = {
#         "status": 0,
#         "message": "success",
#         "data": {}
#     }
#
#     try:
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = Users.query.filter_by(username=username, password=password).first()
#         login_user(user)
#
#     except Exception, e:
#         result['status'] = 1
#         result['message'] = "Login error"
#         app.logger.error(traceback.format_exc())
#
#     return jsonify(result)


@apis.route('/user/accounts', methods=['GET'])
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


@apis.route('/user/account-activities', methods=['POST'])
@login_required
def get_activities():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        get_account = request.form.get('accountNumber')

        if get_account == "1":
            list = []
            for acnt in g.user.accounts:
                list.append(acnt.account_num)
            transactions = db.session.query(Transaction).filter(Transaction.account_num.in_(list)).order_by(
                desc(Transaction.time))
        else:
            if not utils.is_owner(get_account):
                result['status'] = 3
                result['message'] = "You are not the owner of this account."
                return jsonify(result)
            transactions = db.session.query(Transaction).filter(Transaction.account_num == get_account).order_by(
                desc(Transaction.time))

        for trans in transactions:
            tmp = {
                "accountNumber": trans.account_num,
                "dateTime": trans.time,
                "type": trans.type,
                "desc": trans.remark,
                "amount": trans.amount,
                "balanceSnapshot": trans.balance_snapshot
            }
            result['data'].append(tmp)

    except Exception, e:
        result['status'] = 1
        result['message'] = "Get transaction error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)


@apis.route('/user/transactions', methods=['POST'])
@login_required
def get_transactions():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }

    try:
        account_num1 = request.form.get('accountNumber')

        if not utils.is_owner(account_num1):
            result['status'] = 3
            result['message'] = "You are not the owner of this account."
            return jsonify(result)

        transactions = db.session.query(Transaction).filter(Transaction.account_num == account_num1)
        for trans in transactions:
            tmp = {
                "dateTime": trans.time,
                "type": trans.type,
                "desc": trans.remark,
                "amount": trans.amount,
                "balanceSnapshot": trans.balance_snapshot
            }
            result['data'].append(tmp)

    except Exception, e:
        result['status'] = 1
        result['message'] = "Get transaction error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)


@apis.route('/user/transfer', methods=['POST'])
def transfer_funds():
    result = {
        "status": 0,
        "message": "success",
        "data": {}
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
                transf = Transfer(from_account=fromacnt, to_account=toacnt, amount=amt,
                                  time=curr_time)
                db.session.add(transf)
                db.session.commit()
                transf_id = transf.transfer_id

                # insert transaction history record
                transaction_from = Transaction(account_num=fromacnt, amount=-amt, type='transfer',
                                               time=curr_time,
                                               remark='Transfer to ' + toacnt,
                                               operation_id=transf_id,
                                               balance_snapshot=from_account.balance)
                transaction_to = Transaction(account_num=toacnt, amount=amt, type='transfer',
                                             time=curr_time,
                                             remark='Transfer from ' + fromacnt,
                                             operation_id=transf_id,
                                             balance_snapshot=to_account.balance)
                db.session.add(transaction_from)
                db.session.add(transaction_to)
                db.session.commit()
                print "from account: %s,  to account: %s,  amount: %s" % (str(from_account.balance), str(to_account.balance),amt)

            else:
                result['status'] = 2
                result['message'] = "Insufficient funds in from account"
        elif from_account is not None and to_account is None:
            if from_account.balance - amt >= 0:

                from_account.balance -= amt


                # insert transfer record
                transf = Transfer(from_account=fromacnt, to_account=toacnt, amount=amt,
                                  time=curr_time)
                db.session.add(transf)
                db.session.commit()
                transf_id = transf.transfer_id

                # insert transaction history record
                transaction_from = Transaction(account_num=fromacnt, amount=-amt, type='transfer',
                                               time=curr_time,
                                               remark='Transfer to ' + toacnt,
                                               operation_id=transf_id,
                                               balance_snapshot=from_account.balance)
                db.session.add(transaction_from)
                db.session.commit()

        else:
            result['status'] = 3
            result['message'] = "Cannot find account"
    except Exception, e:
        result['status'] = 1
        result['message'] = "Transfer error"
        app.logger.error(traceback.format_exc())

    return jsonify(result)


@apis.route('/user/deposit', methods=['POST'])
def deposit_by_check():
    result = {
        "status": 0,
        "message": "success",
        "data": []
    }
    try:
        # Get parameters
        to_account = request.form.get('toAccount')
        print "to account:" + to_account
        amount = float(request.form.get('amount'))
        check_number = request.form.get('checkNumber')
        memo = request.form.get('memo')
        check_image_front = request.files['checkImageFront']
        check_image_back = request.files['checkImageBack']
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Validate account
        if not utils.has_account(to_account):
            result['status'] = 2
            result['message'] = "Account do not exist"
            return jsonify(result)

        if not utils.is_owner(to_account):
            result['status'] = 2
            result['message'] = "You are not the owner of this account"
            return jsonify(result)

        # save deposit record
        check_image_front_path = base_dir + "/checkImage/" + check_number + "-front.jpg"
        check_image_front.save(check_image_front_path)
        check_image_back_path = base_dir + "/checkImage/" + check_number + "-back.jpg"
        check_image_back.save(check_image_back_path)
        deposit = Deposit(account_num=to_account, amount=amount, check_num=check_number,
                          time=curr_time,
                          img_path_front=check_image_front_path,
                          img_path_back=check_image_back_path)
        db.session.add(deposit)
        db.session.flush()
        # deposit to account
        acnt = db.session.query(Account).filter(Account.account_num == to_account).first()
        acnt.balance += amount
        # save transaction
        transaction_info = Transaction(account_num=to_account, amount=amount, type="deposit",
                                       time=curr_time,
                                       remark="deposit by check: " + check_number + " " + memo,
                                       operation_id=deposit.deposit_id,
                                       balance_snapshot=acnt.balance)
        db.session.add(transaction_info)

        # commit all changes
        db.session.commit()

    except Exception, e:
        result['status'] = 1
        result['message'] = "Some thing happend, check server log."
        app.logger.error(traceback.format_exc())

    return jsonify(result)


@apis.route("/user/profile", methods=['GET', 'POST'])
def user_profile():
    result = {
        "status": 0,
        "message": "success",
        "data": {}
    }
    user_model = db.session.query(Users).filter(Users.user_id == g.user.get_id()).first()
    if request.method == 'GET':
        result['data'] = {
            "ssn": user_model.ssn,
            "username": user_model.username,
            "firstname": user_model.first_name,
            "lastname": user_model.last_name,
            "email": user_model.email,
            "phone": user_model.phone,
            "address": user_model.address,
            "securityQuestion": user_model.security_question,
            "securityAnswer": user_model.security_answer
        }
        return jsonify(result)

    if request.method == 'POST':
        try:
            user_model.ssn = request.form.get("ssn")
            user_model.username = request.form.get("username")
            user_model.first_name = request.form.get("firstname")
            user_model.last_name = request.form.get("lastname")
            user_model.email = request.form.get("email")
            user_model.phone = request.form.get("phone")
            user_model.address = request.form.get("address")
            # user_model.security_question = request.form.get("securityQuestion")
            # user_model.security_answer = request.form.get("securityAnswer")
            db.session.commit()
        except Exception, e:
            result['status'] = 1
            result['message'] = "Get profile error, check your server"
            app.logger.error(traceback.format_exc())
    return jsonify(result)


@apis.route("/user/paybill", methods=['POST'])
def pay_bill_check():
    result = {
        "status": 0,
        "message": "success",
        "data": {}
    }
    try:
        from_account = request.form.get("fromAccount")
        amount = float(request.form.get("amount"))
        biller_name = request.form.get("billerName")
        biller_account = request.form.get("billerAccount")
        biller_address = request.form.get("billerAddress")
        biller_address2 = request.form.get("billerAddress2")
        biller_city = request.form.get("billerCity")
        biller_state = request.form.get("billerState")
        biller_zip = request.form.get("billerZip")
        biller_phone = request.form.get("billerPhone")
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Validate account
        if not utils.has_account(from_account):
            result['status'] = 2
            result['message'] = "Account do not exist"
            return jsonify(result)

        if not utils.is_owner(from_account):
            result['status'] = 2
            result['message'] = "You are not the owner of this account"
            return jsonify(result)

        # Validate and deduct money from account
        account_model = Account.query.filter_by(account_num=from_account).first()
        if account_model.balance < amount:
            result['status'] = 2
            result['message'] = "Insufficient balance in your account."
            return jsonify(result)


        account_model.balance -= amount

        # if biller account in the same bank, add it.
        account_model_biller = Account.query.filter_by(account_num=biller_account).first()
        if account_model_biller:
            account_model_biller.balance += amount

        # save bill record
        bill_model = Bill(from_account=from_account, amount=amount, time=curr_time,
                          biller_name=biller_name, biller_account=biller_account,
                          biller_address="{} {}".format(biller_address, biller_address2),
                          biller_state=biller_state, biller_city=biller_city,
                          biller_zip=biller_zip, biller_phone=biller_phone)
        db.session.add(bill_model)
        db.session.flush()

        # save transaction record
        transaction_model = Transaction(account_num=from_account, amount=-amount, type="bill",
                                        time=curr_time,
                                        remark="pay bill to: {} {}".format(biller_name,
                                                                           biller_account),
                                        operation_id=bill_model.bill_id,
                                        balance_snapshot=account_model.balance)

        db.session.add(transaction_model)
        db.session.commit()

    except Exception, e:
        result['status'] = 1
        result['message'] = "Pay bill failed, check your server."
        app.logger.error(traceback.format_exc())

    return jsonify(result)

@apis.route("/user/enroll/verification", methods=['POST'])
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
            account_info = Account(account_num=any_account, user_id=user_info.user_id, balance=0,
                                   type="", created_time=curr_time)
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


@apis.route("/user/enroll/update", methods=['POST'])
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
