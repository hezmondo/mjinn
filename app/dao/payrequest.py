from datetime import datetime
from app import db
from app.models import PrArrearsMatrix, PrCharge, PrHistory, Rent
from app.modeltypes import PrDeliveryTypes
from app.dao.database import commit_to_database
from sqlalchemy import desc


def add_pr_charge(pr_id, charge_id, case_created):
    pr_charge = PrCharge()
    pr_charge.id = pr_id
    pr_charge.charge_id = charge_id
    pr_charge.case_created = case_created
    db.session.add(pr_charge)


def add_pr_history(pr_history):
    db.session.add(pr_history)
    db.session.flush()
    return pr_history.id


def get_pr_charge(pr_id):
    return PrCharge.query.filter_by(id=pr_id).one_or_none()


def get_pr_file(pr_id):
    pr_file = PrHistory.query.join(Rent).with_entities(PrHistory.id, PrHistory.summary, PrHistory.block,
                                                       PrHistory.datetime, PrHistory.rent_date, PrHistory.total_due,
                                                       Rent.rentcode, Rent.id.label("rent_id")) \
        .filter(PrHistory.id == pr_id).one_or_none()
    return pr_file


def get_pr_history(rent_id):
    return PrHistory.query.filter_by(rent_id=rent_id).order_by(desc(PrHistory.datetime))


def get_recovery_info(suffix):
    recovery_info = PrArrearsMatrix.query.with_entities(PrArrearsMatrix.arrears_clause,
                                                        PrArrearsMatrix.recovery_charge,
                                                        PrArrearsMatrix.create_case). \
        filter_by(suffix=suffix).one_or_none()
    arrears_clause = recovery_info.arrears_clause
    create_case = recovery_info.create_case
    recovery_charge = recovery_info.recovery_charge
    return arrears_clause, create_case, recovery_charge


def post_updated_payrequest(block, pr_id):
    pr_history = PrHistory.query.get(pr_id)
    rent_id = pr_history.rent_id
    pr_history.block = block
    commit_to_database()
    return rent_id


def prepare_new_pr_history_entry(block, pr_save_data, rent_id, mailaddr, method='email'):
    pr_history = PrHistory()
    pr_history.block = block
    pr_history.rent_id = rent_id
    pr_history.summary = pr_save_data.get('pr_code') + "-" + method + "-" + mailaddr[0:25]
    pr_history.datetime = datetime.now()
    pr_history.rent_date = datetime.strptime(pr_save_data.get('rent_date_string'), '%d-%b-%Y')
    pr_history.total_due = pr_save_data.get('tot_due')
    pr_history.arrears_level = pr_save_data.get('new_arrears_level')
    # TODO: We are not using the typeprdelivery table yet in any meaningful way
    #  - should we remove it and make delivery_method in pr_history a string column?
    #  - We'd have to hard code the method strings in any combodict filters
    pr_history.delivery_method = PrDeliveryTypes.get_id(method)
    # TODO: Add pending / delivered functionality
    pr_history.delivered = True
    return pr_history
