import datetime
import os

from flask import render_template, request, redirect, g, url_for, session
from flask_login import current_user, logout_user, login_required

from config import LANGUAGES
from devobs import app, lm
from devobs import babel
from .models import Users

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
@login_required
def account_main():
    return render_template('account-summary.html')


@app.route('/account-activity')
@login_required
def account_activity():
    return render_template('account-activity.html')



@app.route('/transfer')
@app.route('/transfer/')
@app.route('/transfer-own')
@login_required
def transfer_own():
    return render_template('transfer-own.html')


@app.route('/transfer-other')
@login_required
def transfer_other():
    return render_template('transfer-other.html')


@app.route('/transfer-wire')
@login_required
def transfer_wire():
    return render_template('transfer-wire.html')


@app.route('/paybill')
@app.route('/paybill/')
@app.route('/paybill-add')
@login_required
def paybill_add():
    return render_template('paybill-add.html')


@app.route('/paybill-manage')
@login_required
def paybill_manage():
    return render_template('paybill-manage.html')


@app.route('/deposit')
@app.route('/deposit/')
@app.route('/deposit-check')
@login_required
def deposit_check():
    return render_template('deposit-check.html')


@app.route('/loan')
@app.route('/loan/')
@app.route('/loan-summary')
@login_required
def loan_history():
    return render_template('loan-summary.html')


@app.route('/loan-student')
@login_required
def loan_student():
    return render_template('loan-student.html')


@app.route('/loan-equity')
@login_required
def loan_equity():
    return render_template('loan-equity.html')


@app.route('/loan-auto')
@login_required
def loan_auto():
    return render_template('loan-auto.html')


@app.route('/customer-service')
@app.route('/customer-service/')
@app.route("/customer-service-faq")
@login_required
def customer_service_faq():
    return render_template("customer-service-faq.html")


@app.route('/customer-service-contactus')
@login_required
def customer_service_contactus():
    return render_template("customer-service-contactus.html")


@app.route('/customer-service-notification')
@login_required
def customer_service_notification():
    return render_template("customer-service-notification.html")


@app.route('/setting')
@app.route('/setting/')
@app.route('/setting-account')
@login_required
def setting_account():
    return render_template('setting-account.html')


@app.route('/setting-security')
@login_required
def setting_security():
    return render_template('setting-security.html')

# employee website
@app.route('/admin-profile')
def admin_profile():
    return render_template('admin-profile.html')

@app.route('/admin-security')
def admin_security():
    return render_template('admin-security.html')

@app.route('/admin-loan')
def admin_loan():
    return render_template('admin-loan.html')

@app.route('/admin-transfer')
def admin_transfer():
    return render_template('admin-transfer.html')

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
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)
    # session.modified = True
    g.user = current_user


# Internationalization
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
