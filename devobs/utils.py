import hashlib
import os

from flask import g

from devobs import db, app, mail
from devobs.models import Account


def is_owner(account_num):
    acnt = db.session.query(Account).filter(Account.account_num == account_num).first()
    if acnt and acnt.user_id == g.user.user_id:
        return True
    return False


def has_account(account_num):
    acnt = db.session.query(Account).filter(Account.account_num == account_num).first()
    if acnt:
        return True
    return False


def send_email(to_email_addr_list, subject, email_body):
    mail.send_message(subject=subject,
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=to_email_addr_list,
                      html=str(email_body))


def md5(pre_str):
    m = hashlib.md5()
    m.update(pre_str)
    return m.hexdigest()


def generate_random_str():
    return ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(3)))
