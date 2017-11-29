from flask import g
from devobs import db
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
