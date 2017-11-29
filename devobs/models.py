from devobs import db
from passlib.apps import custom_app_context as pwd_context


class Users(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    ssn = db.Column(db.BIGINT, nullable=False, unique=True)
    pin = db.Column(db.Integer, nullable=False, unique=False)
    created_time = db.Column(db.DateTime, nullable=False, unique=False)
    username = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(128), nullable=True, unique=False)
    first_name = db.Column(db.String(64), nullable=True, unique=False)
    last_name = db.Column(db.String(64), nullable=True, unique=False)
    email = db.Column(db.String(64), nullable=True, unique=True)
    phone = db.Column(db.String(64), nullable=True, unique=True)
    address = db.Column(db.String(255), nullable=True, unique=False)
    security_question = db.Column(db.String(255), nullable=True, unique=False)
    security_answer = db.Column(db.String(64), nullable=True, unique=False)
    # relationship columns
    accounts = db.relationship('Account', backref='user', lazy='dynamic')


    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % self.ssn

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class Account(db.Model):
    __tablename__ = 'account'
    account_num = db.Column(db.BIGINT, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.BIGINT, db.ForeignKey('user.user_id'), nullable=False)
    balance = db.Column(db.FLOAT, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    # relationship columns
    transfers = db.relationship('Transfer', backref='account', lazy='dynamic')
    bills = db.relationship('Bill', backref='account', lazy='dynamic')
    deposits = db.relationship('Deposit', backref='account', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic')

    def __repr__(self):
        return '<Account %r>' % self.account_num


class Transfer(db.Model):
    __tablename__ = 'transfer'
    transfer_id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    from_account = db.Column(db.BIGINT, db.ForeignKey('account.account_num'), nullable=False)
    to_account = db.Column(db.BIGINT, nullable=False)
    amount = db.Column(db.FLOAT, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Transfer %r>' % self.transfer_id


class Bill(db.Model):
    __tablename__ = 'bill'
    bill_id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    from_account = db.Column(db.BIGINT, db.ForeignKey('account.account_num'), nullable=False)
    amount = db.Column(db.FLOAT, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    biller_name = db.Column(db.String(64), nullable=False)
    biller_account = db.Column(db.BIGINT, nullable=False)
    biller_address = db.Column(db.String(64), nullable=False)
    biller_city = db.Column(db.String(64), nullable=False)
    biller_state = db.Column(db.String(64), nullable=False)
    biller_zip = db.Column(db.String(64), nullable=False)
    biller_phone = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Bill %r>' % self.bill_id


class Deposit(db.Model):
    __tablename__ = 'deposit'
    deposit_id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    account_num = db.Column(db.BIGINT, db.ForeignKey('account.account_num'), nullable=False)
    amount = db.Column(db.FLOAT, nullable=False)
    check_num = db.Column(db.BIGINT, nullable=False)
    memo = db.Column(db.String(64), nullable=True)
    time = db.Column(db.DateTime, nullable=False)
    img_path_front = db.Column(db.String(255), nullable=False)
    img_path_back = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Deposit %r>' % self.deposit_id


class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    account_num = db.Column(db.BIGINT, db.ForeignKey('account.account_num'), nullable=False)
    amount = db.Column(db.FLOAT, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    time= db.Column(db.DateTime, nullable=False)
    remark = db.Column(db.String(64), nullable=False)
    operation_id = db.Column(db.BIGINT)

    def __repr__(self):
        return '<Transaction %r>' % self.transaction_id
