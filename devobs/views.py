from flask import render_template, request, jsonify, redirect, g, url_for
from flask_login import login_user, login_required, current_user, logout_user
from devobs import app, db, lm
from .models import Users, Transaction, Account, Bill, Transfer, Deposit
import traceback
import time
import os
from devobs import babel
from config import LANGUAGES


base_dir = os.path.abspath(os.path.dirname(__file__))

############# route new template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        print g.user.get_id()
        return redirect((url_for('account_main')))
    else:
        return render_template('customerLogin.html')

@app.route('/admin-login')
def admin_login():
    return render_template('adminLogin.html')

@app.route('/enroll')
def enroll():
    if g.user is not None and g.user.is_authenticated:
        print g.user.get_id()
        return redirect((url_for('account_main')))
    else:
        return render_template('enroll.html')

@app.route('/account')
@app.route('/account/')
@app.route('/account-summary')
def account_main():
    return render_template('account-summary.html')

@app.route('/account-activity')
def account_activity():
    return render_template('account-activity.html')


@app.route('/transfer')
@app.route('/transfer/')
@app.route('/transfer-own')
def transfer_own():
    return render_template('transfer-own.html')

@app.route('/transfer-other')
def transfer_other():
    return render_template('transfer-other.html')

@app.route('/transfer-wire')
def transfer_wire():
    return render_template('transfer-wire.html')

@app.route('/paybill')
@app.route('/paybill/')
@app.route('/paybill-add')
def paybill_add():
    return render_template('paybill-add.html')

@app.route('/paybill-manage')
def paybill_manage():
    return render_template('paybill-manage.html')

@app.route('/deposit')
@app.route('/deposit/')
@app.route('/deposit-check')
def deposit_check():
    return render_template('deposit-check.html')

@app.route('/loan')
@app.route('/loan/')
@app.route('/loan-summary')
def loan_history():
    return render_template('loan-summary.html')

@app.route('/loan-student')
def loan_student():
    return render_template('loan-student.html')

@app.route('/loan-equity')
def loan_equity():
    return render_template('loan-equity.html')

@app.route('/loan-auto')
def loan_auto():
    return render_template('loan-auto.html')


@app.route('/customer-service')
@app.route('/customer-service/')
@app.route("/customer-service-faq")
def customer_service_faq():
    return render_template("customer-service-faq.html")

@app.route('/customer-service-contactus')
def customer_service_contactus():
    return render_template("customer-service-contactus.html")

@app.route('/customer-service-notification')
def customer_service_notification():
    return render_template("customer-service-notification.html")

@app.route('/setting')
@app.route('/setting/')
@app.route('/setting-account')
def setting_account():
    return render_template('setting-account.html')

@app.route('/setting-security')
def setting_security():
    return render_template('setting-security.html')


#############


#
# @app.route('/index2')
# @login_required
# def index():
#     return render_template('index2.html')
#
# @app.route('/account-activity2')
# @login_required
# def balance():
#     return render_template('account-activity2.html')
#
# @app.route('/deposit')
# @login_required
# def deposit():
#     return render_template('deposit.html')
#
#
# @app.route('/transfer')
# @login_required
# def transfer():
#     return render_template('transfer.html')
#
# @app.route('/billpay')
# @login_required
# def billpay():
#     return render_template('billpay.html')
#
# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.before_request
def befor_reques():
    g.user = current_user


# Internationalization
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())