from app import db, cache
from flask import request
from sqlalchemy.orm import load_only
from app.dao.database import commit_to_database
from app.models import Agent, Case, Charge, ChargeType, Date_m, DocFile, DigFile, EmailAcc, FormLetter, Income, \
    IncomeAlloc, Landlord, LeaseUpType, Loan, MoneyItem, Property, PrCharge, PrHistory, Rent, RentExternal, MoneyAcc, \
    TypeAcType, TypeAdvArr, TypeDeed, TypeDoc, TypeEvent, TypeFreq, TypeMailTo, TypePayment, TypePrDelivery, \
    TypeProperty, TypeSaleGrade, TypeStatus, TypeStatusBatch, TypeStatusHr, TypeTenure


def delete_record(item_id, item):
    id_2 = request.args.get('id_2')
    id_dict = {}
    redir = "util_bp.home"
    if item == "agent":
        Agent.query.filter_by(id=item_id).delete()
        redir = "util_bp.agents"
    elif item == "case":
        Case.query.filter_by(id=item_id).delete()
        redir = "rent_bp.rent"
    elif item == "charge":
        Charge.query.filter_by(id=item_id).delete()
        redir = "rent_bp.rent"
        id_dict = {"id": id_2}
    elif item == "doc":
        DocFile.query.filter_by(id=item_id).delete()
        redir = "doc_bp.docfiles"
    elif item == "dig":
        DigFile.query.filter_by(id=item_id).delete()
        redir = "doc_bp.docfiles"
    elif item == "email_acc":
        EmailAcc.query.filter_by(id=item_id).delete()
        redir = "util_bp.email_accs"
    elif item == "formletter":
        FormLetter.query.filter_by(id=item_id).delete()
        redir = "formletter_bp.forms"
    elif item == "income":
        Income.query.filter_by(id=item_id).delete()
        redir = "income_bp.income"
    elif item == "incomealloc":
        IncomeAlloc.query.filter_by(id=item_id).delete()
        redir = "income_bp.income"
    elif item == "landlord":
        Landlord.query.filter_by(id=item_id).delete()
        redir = "landlord_bp.landlords"
    elif item == "loan":
        Loan.query.filter_by(id=item_id).delete()
        redir = "loan_bp.loans"
    elif item == "money_acc":
        MoneyAcc.query.filter_by(id=item_id).delete()
        redir = "money_bp.moneyaccs"
    elif item == "money_item":
        MoneyItem.query.filter_by(id=item_id).delete()
        redir = "money_bp.money_items"
        id_dict = {"id": id_2}
    elif item == "pr_charge":
        PrCharge.query.filter_by(id=item_id).delete()
        redir = "pr_bp.pr_history"
    elif item == "property":
        Property.query.filter_by(id=item_id).delete()
        redir = "properties"
    elif item == "pr_file":
        PrHistory.query.filter_by(id=item_id).delete()
        redir = "pr_bp.pr_history"
        id_dict = {"rent_id": id_2}
    elif item == "rent":
        Rent.query.filter_by(id=item_id).delete()
    elif item == "rent_external":
        RentExternal.query.filter_by(id=item_id).delete()
    commit_to_database()
    return redir, id_dict


def delete_record_basic(item_id, item):
    if item == "case":
        Case.query.filter_by(id=item_id).delete()
    elif item == "charge":
        Charge.query.filter_by(id=item_id).delete()
    elif item == "pr_charge":
        PrCharge.query.filter_by(id=item_id).delete()
    elif item == "pr_file":
        PrHistory.query.filter_by(id=item_id).delete()


@cache.cached(key_prefix='db_actypes_all')
def get_actypes():
    actypes = TypeAcType.query.all()

    return actypes


@cache.cached(key_prefix='db_advarr_types_all')
def get_advarr_types():
    advarr_types = TypeAdvArr.query.all()

    return advarr_types


@cache.cached(key_prefix='db_batchstatus_types_all')
def get_batchstatus_types():
    batchstatus_types = TypeStatusBatch.query.all()

    return batchstatus_types


@cache.cached(key_prefix='db_charge_types_all')
def get_charge_types():
    charge_types = ChargeType.query.all()

    return charge_types


@cache.cached(key_prefix='db_dates_m_all')
def get_dates_m():
    dates_m = Date_m.query.with_entities(Date_m.code_id, Date_m.month, Date_m.day).all()

    return dates_m


def get_deed(deed_id):
    deed = TypeDeed.query.get(deed_id)

    return deed


def get_deed_types():
    deed_types = TypeDeed.query.all()

    return deed_types


def get_doctype(doctype_id):   #returns desc as doctype
    return db.session.query(TypeDoc).filter_by(id=doctype_id).options(load_only('desc')).one_or_none()


@cache.cached(key_prefix='db_doc_types_all')
def get_doc_types():
    doc_types = TypeDoc.query.all()

    return doc_types


def get_event_types():
    event_types = TypeEvent.query.all()

    return event_types


@cache.cached(key_prefix='db_freq_types_all')
def get_freq_types():
    freq_types = TypeFreq.query.all()

    return freq_types


def get_hrstatus_types():
    hrstatus_types = TypeStatusHr.query.all()

    return hrstatus_types


def get_mailto_types():
    mailto_types = TypeMailTo.query.all()

    return mailto_types


def get_pay_types():
    pay_types = TypePayment.query.all()

    return pay_types


def get_prdelivery_types():
    prdelivery_types = TypePrDelivery.query.all()

    return prdelivery_types


def get_prop_types():
    prop_types = TypeProperty.query.all()

    return prop_types


def get_salegrade_types():
    salegrade_types = TypeSaleGrade.query.all()

    return salegrade_types


def get_status_types():
    status_types = TypeStatus.query.all()

    return status_types


@cache.cached(key_prefix='db_tenure_types_all')
def get_tenure_types():
    status_types = TypeTenure.query.all()

    return status_types


def get_uplift_types():
    uplift_types = LeaseUpType.query.all()

    return uplift_types


def post_deed(deed_id, rent_id):
    if deed_id == 0:
        deed = TypeDeed()
    else:
        deed = TypeDeed.query.get(deed_id)
    deed.deedcode = request.form.get("deedcode")
    deed.nfee = request.form.get("nfee")
    deed.nfeeindeed = request.form.get("nfeeindeed")
    deed.info = request.form.get("info")
    db.session.add(deed)
    db.session.flush()
    deed_id = deed.id
    if rent_id != 0:
        rent = Rent.query.get(rent_id)
        rent.deed_id = deed_id
    commit_to_database()

    return deed_id
