from apscheduler.schedulers.blocking import BlockingScheduler

from devobs import db, utils
from .models import Users


def check_all_user_balance():
    users = db.session.query(Users).all()
    print users
    for user in users:
        for account in user.accounts:
            if account.balance < 100:
                email_body = "<p> Your balance for account <b>{account}</b> is only <b>{balance}</b>. Please make sure the balance is correct and enough. If you have any question, please contact us at 1-080-987-6541, Monday through Friday 7 am to 10pm, Saturday and Sunday 8 am to 5 pm ET. This email was sent automatically as an additional layer of security. Thank you for using Devonshire Lending. This mailbox is not monitored. Please do not reply.</p>".format(
                    balance=account.balance, account=account.account_num)
                utils.send_email(user.email, "Watch out your account balance!", email_body)


def auto_check():
    scheduler = BlockingScheduler()
    # it will check all the account every day 6:30 am, from Mon to Fri
    scheduler.add_job(check_all_user_balance, 'cron', day_of_week='1-5', hour=6, minute=30)
    scheduler.start()

