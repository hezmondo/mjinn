import sqlalchemy
from app import db
from flask import request
from sqlalchemy import func
from app.dao.database import commit_to_database
from app.models import Loan, LoanStat
from app.modeltypes import AdvArr, Freqs


def get_loan(loan_id):
    if request.method == "POST":
        loan_id = post_loan(loan_id)
    if loan_id != 0:
        loan = db.session.query(Loan).filter_by(id=loan_id).first()
        loan.freqdet = Freqs.get_name(loan.freq_id)
    else:
        loan = Loan()
        loan.id = 0

    return loan


def get_loans(action):
    if action == "Nick":
        loans = Loan.query.with_entities(Loan.id, Loan.code, Loan.interest_rate, Loan.end_date, Loan.lender,
                                         Loan.borrower,
                                         Loan.notes, Loan.val_date, Loan.valuation, Loan.interestpa) \
            .filter(Loan.lender.ilike('%NJL%')).all()
        loansum = Loan.query.with_entities(func.sum(Loan.valuation).label('tot_val'),
                                           func.sum(Loan.interestpa).label('totint')) \
            .filter(Loan.lender.ilike('%NJL%')).first()
    else:
        loans = Loan.query.with_entities(Loan.id, Loan.code, Loan.interest_rate, Loan.end_date, Loan.lender,
                                         Loan.borrower,
                                         Loan.notes, Loan.val_date, Loan.valuation, Loan.interestpa).all()
        loansum = Loan.query.with_entities(func.sum(Loan.valuation).label('tot_val'),
                                           func.sum(Loan.interestpa).label('totint')).filter().first()

    return loans, loansum


def post_loan(loan_id):
    loan = Loan.query.get(loan_id) or Loan()
    loan.code = request.form.get("loancode")
    loan.interest_rate = request.form.get("interest_rate")
    loan.end_date = request.form.get("end_date")
    loan.freq_id = Freqs.get_id(request.form.get("frequency"))
    loan.advarr_id = AdvArr.get_id(request.form.get("advarr"))
    loan.lender = request.form.get("lender")
    loan.borrower = request.form.get("borrower")
    loan.notes = request.form.get("notes")
    # loan.val_date = request.form.get("val_date")
    # loan.valuation = request.form.get("valuation")
    # delete_loan_trans = LoanTran.query.filter(LoanTran.loan_id == id).all()
    # delete_loan_interest_rate = LoanIntRate.query.filter(LoanIntRate.loan_id == id).all()
    # db.session.delete(delete_loan_interest_rate)
    # db.session.delete(delete_loan_trans)
    db.session.add(loan)
    db.session.flush()
    loan_id = loan.id
    commit_to_database()

    return loan_id


def get_loan_statement(loan_id):
    stat_date = request.form.get("statdate")
    rproxy = db.session.execute(sqlalchemy.text("CALL pop_loan_statement(:x, :y)"),
                                params={"x": loan_id, "y": stat_date})
    checksums = rproxy.fetchall()
    db.session.commit()
    loanstatement = LoanStat.query.with_entities(LoanStat.id, LoanStat.date, LoanStat.memo,
                                                 LoanStat.transaction, LoanStat.rate,
                                                 LoanStat.interest,
                                                 LoanStat.add_interest, LoanStat.balance).all()
    loan = Loan.query.get(loan_id)
    loancode = loan.code

    return checksums, loancode, loanstatement
