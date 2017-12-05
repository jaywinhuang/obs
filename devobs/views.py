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


@app.route("/customer-service/faq")
@app.route('/customer-service')
def customer_service_faq():
    return render_template("customer-service-faq.html")

@app.route('/customer-service/contactus')
def customer_service_contactus():
    return render_template("customer-service-contactus.html")\

@app.route('/customer-service/notification')
def customer_service_notification():
    return render_template("customer-service-notification.html")


#############



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
@login_required
def deposit():
    return render_template('deposit.html')


@app.route('/transfer')
@login_required
def transfer():
    return render_template('transfer.html')

@app.route('/billpay')
@login_required
def billpay():
    return render_template('billpay.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        print g.user.get_id()
        return redirect((url_for('index')))
    else:
        return render_template('login.html')

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