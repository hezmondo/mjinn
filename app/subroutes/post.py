# from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import asc, desc, extract, func, literal, and_, or_
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_password_reset_email
from app.forms import EditProfileForm, LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import Agent, Charge, Chargetype, Datef2, Datef4, Extmanager, Extrent, Income, Incomealloc, \
    Landlord, Manager, Property, Rent, Typeactype, Typeadvarr, Typebankacc, Typedeed, Typefreq, Typemailto, \
    Typepayment, Typeproperty, Typesalegrade, Typestatus, Typetenure, User, Emailaccount


def postcharge(id):
    charge = Charge.query.get(id)
    charge.chargetype_id = \
        Chargetype.query.with_entities(Chargetype.id).filter(
            Chargetype.chargedesc == request.form["chargedesc"]).one()[0]
    charge.chargestartdate = request.form["chargestartdate"]
    charge.chargetotal = request.form["chargetotal"]
    charge.chargedetails = request.form["chargedetails"]
    charge.chargebalance = request.form["chargebalance"]
    db.session.commit()
    return


def postemailacc(id):
    if id > 0:
        emailacc = Emailaccount.query.get(id)
    else:
        emailacc = Emailaccount()
    emailacc.smtp_server = request.form["smtp_server"]
    emailacc.smtp_port = request.form["smtp_port"]
    emailacc.smtp_timeout = request.form["smtp_timeout"]
    emailacc.smtp_debug = request.form["smtp_debug"]
    emailacc.smtp_tls = request.form["smtp_tls"]
    emailacc.smtp_user = request.form["smtp_user"]
    emailacc.smtp_password = request.form["smtp_password"]
    emailacc.smtp_sendfrom = request.form["smtp_sendfrom"]
    emailacc.imap_server = request.form["imap_server"]
    emailacc.imap_port = request.form["imap_port"]
    emailacc.imap_tls = request.form["imap_tls"]
    emailacc.imap_user = request.form["imap_user"]
    emailacc.imap_password = request.form["imap_password"]
    emailacc.imap_sentfolder = request.form["imap_sentfolder"]
    emailacc.imap_draftfolder = request.form["imap_draftfolder"]
    if id == 0:
        db.session.add(emailacc)
        db.session.commit()
        id = emailacc.id
        return
    else:
        db.session.commit()
        return


def postlandlord(id):
    if id > 0:
        landlord = Landlord.query.get(id)
    else:
        landlord = Landlord()
    landlord.name = request.form["name"]
    landlord.addr = request.form["address"]
    landlord.taxdate = request.form["taxdate"]
    emailacc = request.form["emailacc"]
    landlord.emailacc_id = \
        Emailaccount.query.with_entities(Emailaccount.id).filter \
            (Emailaccount.smtp_server == emailacc).one()[0]
    bankacc = request.form["bankacc"]
    landlord.bankacc_id = \
        Typebankacc.query.with_entities(Typebankacc.id).filter \
            (Typebankacc.accnum == bankacc).one()[0]
    manager = request.form["manager"]
    landlord.manager_id = \
        Manager.query.with_entities(Manager.id).filter \
            (Manager.name == manager).one()[0]
    if id < 1:
        db.session.add(landlord)
        db.session.commit()
        id = landlord.id
    db.session.commit()
    return


def postrentobj(id):
    if id > 0:
        rent = Rent.query.get(id)
        property = Property.query.filter(Property.rent_id == id).first()
        agent = Agent.query.filter(Agent.id == rent.agent_id).one_or_none()
    else:
        rent = Rent()
        property = Property()
        agent = Agent()

    actype = request.form["actype"]
    rent.actype_id = \
        Typeactype.query.with_entities(Typeactype.id).filter(Typeactype.actypedet == actype).one()[0]
    advarr = request.form["advarr"]
    rent.advarr_id = \
        Typeadvarr.query.with_entities(Typeadvarr.id).filter(Typeadvarr.advarrdet == advarr).one()[0]
    rent.arrears = request.form["arrears"]

    # we will write code later to generate datecode from lastrentdate!:
    rent.datecode = request.form["datecode"]

    deedtype = request.form["deedtype"]
    rent.deed_id = \
        Typedeed.query.with_entities(Typedeed.id).filter(Typedeed.deedcode == deedtype).one()[0]
    rent.email = request.form["email"]
    frequency = request.form["frequency"]
    rent.freq_id = \
        Typefreq.query.with_entities(Typefreq.id).filter(Typefreq.freqdet == frequency).one()[0]
    landlord = request.form["landlord"]
    rent.landlord_id = \
        Landlord.query.with_entities(Landlord.id).filter(Landlord.name == landlord).one()[0]
    rent.lastrentdate = request.form["lastrentdate"]
    mailto = request.form["mailto"]
    rent.mailto_id = \
        Typemailto.query.with_entities(Typemailto.id).filter(Typemailto.mailtodet == mailto).one()[0]
    rent.note = request.form["note"]
    rent.price = request.form["price"]
    rent.rentpa = request.form["rentpa"]
    salegrade = request.form["salegrade"]
    rent.salegrade_id = \
        Typesalegrade.query.with_entities(Typesalegrade.id).filter(Typesalegrade.salegradedet == salegrade).one()[0]
    rent.source = request.form["source"]
    status = request.form["status"]
    rent.status_id = \
        Typestatus.query.with_entities(Typestatus.id).filter(Typestatus.statusdet == status).one()[0]
    rent.tenantname = request.form["tenantname"]
    tenure = request.form["tenure"]
    rent.tenure_id = \
        Typetenure.query.with_entities(Typetenure.id).filter(Typetenure.tenuredet == tenure).one()[0]

    agdetails = request.form["agent"]
    if agdetails and agdetails != "None":
        if not agent:
            agent = Agent()
            agent.agdetails = agdetails
            agent.rent_agent.append(rent)
            db.session.add(agent)
        else:
            agent.agdetails = agdetails
    property.propaddr = request.form["propaddr"]
    proptype = request.form["proptype"]
    property.typeprop_id = \
        Typeproperty.query.with_entities(Typeproperty.id).filter(Typeproperty.proptypedet == proptype).one()[0]
    if id < 1:
        rent.rentcode = request.form["rentcode"]
        rent.prop_rent.append(property)
        db.session.add(rent)
    # lots of challenges: I have allowed for editing an existing agent, but not switching to another or new agent
    # I have not dealt with case where someone simply deletes all existing agentdetails
    db.session.commit()
    return


def postagent(id):
    agent = Agent.query.get(id)
    agent.agdetails = request.form["address"]
    agent.agemail = request.form["email"]
    agent.agnotes = request.form["notes"]
    db.session.commit()
    return