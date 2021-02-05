from app import db
from flask import request
from app.dao.functions import commit_to_database

from app.models import Landlord, Manager, Money_account, EmailAcc


def delete_landlord(landlord_id):
    Landlord.query.filter_by(id=landlord_id).delete()
    commit_to_database()


def get_landlords():
    landlords = Landlord.query.join(Manager).with_entities(Landlord.id, Landlord.name, Landlord.address,
                                                           Landlord.tax_date, Manager.managername).all()
    return landlords


def get_landlord(id):

    landlord = Landlord.query.join(Manager).join(EmailAcc).join(Money_account).with_entities(Landlord.id,
                                                                                             Landlord.name, Landlord.address, Landlord.tax_date, Manager.managername,
                                                                                             EmailAcc.smtp_server, Money_account.acc_desc) \
        .filter(Landlord.id == id).one_or_none()
    return landlord


def get_landlord_dict():
    managers = [value for (value,) in Manager.query.with_entities(Manager.managername).all()]
    emailaccs = [value for (value,) in EmailAcc.query.with_entities(EmailAcc.smtp_server).all()]
    acc_descs = [value for (value,) in Money_account.query.with_entities(Money_account.acc_desc).all()]
    landlord_dict = {
        "managers": managers,
        "emailaccs": emailaccs,
        "acc_descs": acc_descs
    }
    return landlord_dict


def post_landlord(id):
    if id == 0:
        landlord = Landlord()
        landlord.id = 0
    else:
        landlord = Landlord.query.get(id)
    ll_name = request.form.get("name")
    landlord.name = ll_name
    landlord.address = request.form.get("address")
    landlord.tax_date = request.form.get("tax_date")
    emailacc = request.form.get("emailacc")
    landlord.email_acc_id = \
        EmailAcc.query.with_entities(EmailAcc.id).filter \
            (EmailAcc.smtp_server == emailacc).one()[0]
    acc_desc = request.form.get("acc_desc")
    landlord.acc_id = \
        Money_account.query.with_entities(Money_account.id).filter \
            (Money_account.acc_desc == acc_desc).one()[0]
    manager = request.form.get("manager")
    landlord.manager_id = \
        Manager.query.with_entities(Manager.id).filter \
            (Manager.managername == manager).one()[0]
    db.session.add(landlord)
    commit_to_database()
    landlord = Landlord.query.filter(Landlord.name == ll_name).first()
    return landlord
