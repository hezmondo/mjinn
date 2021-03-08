import json
from decimal import Decimal
from app import db
from flask import flash, redirect, url_for, request
from sqlalchemy import func
from app.main.common import get_postvals_id, inc_date_m
from app.dao.database import pop_idlist_recent
from app.main.functions import strToDec
from app.models import Agent, Charge, Jstore, Landlord, Manager, ManagerExt, MoneyAcc, Property, \
    Rent, RentExt, TypeAcType, TypeAdvArr, TypeDeed, TypeFreq, TypeMailTo, TypePrDelivery, TypeSaleGrade, \
    TypeStatus, TypeTenure


def create_new_rent():
    # create new rent and property function not yet built, so return id for dummy rent:

    return 23


def get_rent(rent_id):
    if rent_id == 0:
        # take the user to create new rent function:
        rent_id = create_new_rent()
    rent_ = \
        Rent.query \
            .join(Landlord) \
            .join(Manager) \
            .outerjoin(Agent) \
            .join(TypeAcType) \
            .join(TypeAdvArr) \
            .join(TypeDeed) \
            .join(TypeFreq) \
            .join(TypeMailTo) \
            .join(TypePrDelivery) \
            .join(TypeSaleGrade) \
            .join(TypeStatus) \
            .join(TypeTenure) \
            .with_entities(Rent.id, Rent.rentcode, Rent.arrears, Rent.datecode_id, Rent.email, Rent.lastrentdate,
                           func.mjinn.mail_addr(Rent.id).label('mailaddr'),
                           func.mjinn.paid_to_date(Rent.id).label('paidtodate'),
                           func.mjinn.prop_addr(Rent.id).label('propaddr'),
                           func.mjinn.tot_charges(Rent.id).label('totcharges'),
                           Rent.note, Rent.price, Rent.rentpa, Rent.source, Rent.tenantname, Rent.freq_id,
                           Agent.id.label("agent_id"), Agent.detail, Landlord.name, Manager.managername,
                           Manager.manageraddr,
                           TypeAcType.actypedet, TypeAdvArr.advarrdet, TypeDeed.deedcode, TypeDeed.info,
                           TypeFreq.freqdet, TypeMailTo.mailtodet, TypePrDelivery.prdeliverydet,
                           TypeSaleGrade.salegradedet, TypeStatus.statusdet, TypeTenure.tenuredet) \
            .filter(Rent.id == rent_id) \
            .one_or_none()
    if rent_ is None:
        flash('Invalid rent code')
        return redirect(url_for('auth.login'))
    else:
        pop_idlist_recent("recent_rents", rent_id)

    return rent_


def get_rent_addrs(rent_id):
    rent_addrs = \
        Rent.query.join(TypeMailTo).with_entities(Rent.id, Rent.rentcode, Rent.tenantname,
                                                  func.mjinn.mail_addr(Rent.id).label('mailaddr'),
                                                  func.mjinn.prop_addr(Rent.id).label('propaddr'),
                                                  func.mjinn.tot_charges(Rent.id).label('totcharges'),
                                                  TypeMailTo.mailtodet) \
            .filter(Rent.id == rent_id) \
            .one_or_none()
    if rent_addrs is None:
        flash('Invalid rent code')

        return redirect(url_for('auth.login'))

    return rent_addrs


def get_rent_ex(id):
    rent_ex = RentExt.query \
        .join(ManagerExt) \
        .with_entities(RentExt.rentcode, RentExt.propaddr, RentExt.tenantname, RentExt.owner, RentExt.rentpa,
                       RentExt.arrears, RentExt.lastrentdate, RentExt.source, RentExt.status,
                       ManagerExt.codename, ManagerExt.detail, RentExt.agentdetail) \
        .filter(RentExt.id == id).one_or_none()
    return rent_ex


def get_rent_mail(rent_id):
    rent_mail = \
        Rent.query \
            .join(Landlord) \
            .join(Manager) \
            .join(MoneyAcc) \
            .join(TypeAdvArr) \
            .join(TypeFreq) \
            .join(TypeStatus) \
            .join(TypeTenure) \
            .with_entities(Rent.id, Rent.rentcode, Rent.arrears, Rent.datecode_id, Rent.email, Rent.lastrentdate,
                           func.mjinn.check_pr_exists(Rent.id).label('prexists'),
                           func.mjinn.mail_addr(Rent.id).label('mailaddr'),
                           func.mjinn.paid_to_date(Rent.id).label('paidtodate'),
                           func.mjinn.prop_addr(Rent.id).label('propaddr'),
                           func.mjinn.tot_charges(Rent.id).label('totcharges'),
                           func.mjinn.last_arrears_level(Rent.id).label('lastarrearslevel'),
                           Rent.price, Rent.rentpa, Rent.tenantname, Rent.freq_id, Landlord.name,
                           Manager.managername, Manager.manageraddr, Manager.manageraddr2,
                           MoneyAcc.bank_name, MoneyAcc.acc_name, MoneyAcc.acc_num, MoneyAcc.sort_code,
                           TypeAdvArr.advarrdet, TypeFreq.freqdet, TypeStatus.statusdet, TypeTenure.tenuredet) \
            .filter(Rent.id == rent_id) \
            .one_or_none()

    return rent_mail


def get_rent_s_data(qfilter, action, runsize):
    if action == "basic":
        # simple search of views rents submitted from home page
        # Sam: I have removed inc_date_m and am using a class RentS in utility.py to derive the nextrentdate from
        # the inc_date_m python function
        rent_s = \
            Property.query \
                .join(Rent) \
                .outerjoin(Agent) \
                .with_entities(Rent.id, Agent.detail, Rent.arrears, Rent.freq_id, Rent.lastrentdate, Rent.datecode_id,
                               # func.mjinn.inc_date_m(Rent.lastrentdate, Rent.freq_id, Rent.datecode_id,
                               #                           1).label('nextrentdate'),
                               Property.propaddr, Rent.rentcode, Rent.rentpa, Rent.source, Rent.tenantname) \
                .filter(*qfilter).limit(runsize).all()

    elif action == "external":
        # simple search of external rents submitted from home page - not yet completed
        rent_s = \
            RentExt.query \
            .join(ManagerExt) \
            .with_entities(RentExt.id, RentExt.rentcode, RentExt.propaddr, RentExt.tenantname, RentExt.owner,
                           RentExt.rentpa, RentExt.arrears, RentExt.lastrentdate, RentExt.source, RentExt.status,
                           ManagerExt.codename, RentExt.agentdetail) \
            .filter(*qfilter).order_by(RentExt.rentcode).limit(runsize).all()

    else:
        # advanced search submitted from filter page
        rent_s = \
                Property.query \
                    .join(Rent) \
                    .join(Landlord) \
                    .outerjoin(Agent) \
                    .outerjoin(Charge) \
                    .join(TypeAcType) \
                    .join(TypePrDelivery) \
                    .join(TypeStatus) \
                    .join(TypeSaleGrade) \
                    .join(TypeTenure) \
                    .with_entities(Rent.id, TypeAcType.actypedet, Agent.detail, Rent.arrears, Rent.lastrentdate,
                            func.mjinn.inc_date_m(Rent.lastrentdate,
                                                  Rent.freq_id, Rent.datecode_id, 1).label('nextrentdate'),
                            func.mjinn.tot_charges(Rent.id).label('totcharges'), Landlord.name, Property.propaddr,
                            Rent.rentcode, Rent.rentpa, Rent.source, Rent.tenantname,
                            TypePrDelivery.prdeliverydet, TypeSaleGrade.salegradedet, TypeStatus.statusdet,
                            TypeTenure.tenuredet) \
                    .filter(*qfilter).order_by(Rent.rentcode).limit(runsize).all()

    return rent_s


def post_rent__filter(filterdict):
    # save this filter dictionary in jstore
    print("filterdict during save")
    print(filterdict)
    jname = request.form.get("filtername")
    jtype = request.form.get("filtertype")
    if jtype == "payrequest":
        jtype = 1
    elif jtype == "rentprop":
        jtype = 2
    else:
        jtype = 3
    j_id = \
        Jstore.query.with_entities(Jstore.id).filter \
            (Jstore.code == jname).one_or_none()
    if j_id:
        j_id = j_id[0]
        jstore = Jstore.query.get(j_id)
    else:
        jstore = Jstore()
    jstore.type = jtype
    jstore.code = jname
    jstore.content = json.dumps(filterdict)
    db.session.add(jstore)
    db.session.commit()


def post_rent(rent_id):
    rent = Rent.query.get(rent_id)
    postvals_id = get_postvals_id()
    # we need the post values with the class id generated for the actual combobox values:
    rent.actype_id = postvals_id["actype"]
    rent.advarr_id = postvals_id["advarr"]
    rent.arrears = strToDec(request.form.get("arrears"))
    # we need code to generate datecode_id from lastrentdate with user choosing sequence:
    rent.datecode_id = int(request.form.get("datecode_id"))
    rent.deed_id = postvals_id["deedcode"]
    rent.freq_id = postvals_id["frequency"]
    rent.landlord_id = postvals_id["landlord"]
    rent.lastrentdate = request.form.get("lastrentdate")
    price = request.form.get("price")
    rent.price = price if (price and price != 'None') else Decimal(99999)
    rent.rentpa = strToDec(request.form.get("rentpa"))
    rent.salegrade_id = postvals_id["salegrade"]
    rent.source = request.form.get("source")
    rent.status_id = postvals_id["status"]
    rent.tenure_id = postvals_id["tenure"]
    db.session.add(rent)
    db.session.flush()
    rent_id = rent.id
    db.session.commit()

    return rent_id


# def update_roll_rent(rent_id, arrears):
#     rent = Rent.query.get(rent_id)
#  this fn now gone!  last_rent_date = db.session.execute(func.mjinn.next_rent_date(rent.id, 1, 1)).scalar()
#     rent.lastrentdate = last_rent_date
#     rent.arrears = arrears


def update_roll_rent(rent_id, last_rent_date, arrears):
    rent = Rent.query.get(rent_id)
    rent.lastrentdate = last_rent_date
    rent.arrears = arrears


def update_rollback_rent(rent_id, arrears):
    rent = Rent.query.get(rent_id)
    last_rent_date = inc_date_m(rent.lastrentdate, rent.freq_id, rent.datecode_id, -1)
    rent.lastrentdate = last_rent_date
    rent.arrears = arrears


# def update_roll_rents(rent_mails):
#     update_vals = []
#     for rent_mailop in rent_mails:
#         update_vals.append(update_roll_rent(rent_mailop.id))
#     db.session.bulk_update_mappings(Rent, update_vals)


def update_tenant(rent_id):
    rent = Rent.query.get(rent_id)
    rent.tenantname = request.form.get("tenantname")
    postvals_id = get_postvals_id()
    rent.mailto_id = postvals_id["mailto"]
    rent.email = request.form.get("email")
    rent.prdelivery_id = postvals_id["prdelivery"]
    rent.note = request.form.get("note")
    db.session.add(rent)
    db.session.commit()

