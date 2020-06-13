from flask import redirect, request

from app import db
from app.models import Agent, Charge, Chargetype, Date_f2, Date_f4, Extmanager, Extrent, Income, Incomealloc, \
    Landlord, Loan, Manager, Money_category, Money_item, Property, Rent, Rental, \
    Typeactype, Typeadvarr, Money_account, Typedeed, Typefreq, \
    Typemailto, Typepayment, Typeproperty, Typesalegrade, Typestatus, Typetenure, User, Emailaccount


def postagent(id):
    if id and id > 0 :
        agent = Agent.query.get(id)
    else:
        agent = Agent()
    agent.agdetails = request.form["address"]
    agent.agemail = request.form["email"]
    agent.agnotes = request.form["notes"]
    if id == 0 or id is None:
        db.session.add(agent)
        db.session.commit()
        id = agent.id
    else:
        db.session.commit()

    return redirect('/agentpage/{}'.format(id))


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


def postemailacc(id, action):
    if action == "edit":
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
    if not action == "edit":
        db.session.add(emailacc)
        db.session.commit()
        id = emailacc.id
    else:
        db.session.commit()

    return redirect('/emailaccpage/{}'.format(id))


def postincome(id, action):
    if action == "edit":
        income = Income.query.get(id)
    else:
        income = Income()
    if not action == "edit":
        db.session.add(income)
        db.session.commit()
        id = income.id
    else:
        db.session.commit()

    return redirect('/incomepage/{}'.format(id))


def postincomealloc(id, action):
    if action == "edit":
        income = Income.query.get(id)
    else:
        income = Income()
    if not action == "edit":
        db.session.add(income)
        db.session.commit()
        id = income.id
    else:
        db.session.commit()

    return redirect('/incomepage/{}'.format(id))


def postlandlord(id, action):
    if action == "edit":
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
        Money_account.query.with_entities(Money_account.id).filter \
            (Money_account.accdesc == bankacc).one()[0]
    manager = request.form["manager"]
    landlord.manager_id = \
        Manager.query.with_entities(Manager.id).filter \
            (Manager.name == manager).one()[0]
    db.session.add(landlord)
    db.session.commit()
    id_ = landlord.id
    return id_


def postloan(id):
    if id > 0:
        loan = Loan.query.get(id)
    else:
        loan = Loan()
    loan.code = request.form["loancode"]
    loan.start_intrate = request.form["start_intrate"]
    loan.end_date = request.form["end_date"]
    frequency = request.form["frequency"]
    loan.freq_id = \
        Typefreq.query.with_entities(Typefreq.id).filter(Typefreq.freqdet == frequency).one()[0]
    advarr = request.form["advarr"]
    loan.advarr_id = \
        Typeadvarr.query.with_entities(Typeadvarr.id).filter(Typeadvarr.advarrdet == advarr).one()[0]
    loan.lender = request.form["lender"]
    loan.borrower = request.form["borrower"]
    loan.notes = request.form["notes"]
    loan.val_date = request.form["val_date"]
    loan.valuation = request.form["valuation"]
    db.session.commit()
    return


def post_moneyaccount(id, action):
    if action == "edit":
        account = Money_account.query.get(id)
    else:
        account = Money_account()
    account.bankname = request.form["bankname"]
    account.accname = request.form["accname"]
    account.sortcode = request.form["sortcode"]
    account.accnum = request.form["accnum"]
    account.accdesc = request.form["accdesc"]
    db.session.add(account)
    db.session.commit()
    id_ = account.id

    return id_


def post_moneyitem(id, action):
    if action == "edit":
        bankitem = Money_item.query.get(id)
    else:
        bankitem = Money_item()
    bankitem.num = request.form["num"]
    bankitem.date = request.form["date"]
    bankitem.amount = request.form["amount"]
    bankitem.payer = request.form["payer"]
    accdesc = request.form["accdesc"]
    bankitem.bankacc_id = \
        Money_account.query.with_entities(Money_account.id).filter \
            (Money_account.accdesc == accdesc).one()[0]
    cleared = request.form["cleared"]
    bankitem.cleared = 1 if cleared == "cleared" else 0
    cat = request.form["category"]
    bankitem.cat_name = \
        Money_category.query.with_entities(Money_category.id).filter \
            (Money_category.cat_name == cat).one()[0]
    db.session.add(bankitem)
    db.session.commit()
    id_ = bankitem.id

    return id_


def postproperty(id):
    property = Property.query.get(id)
    property.propaddr = request.form["propaddr"]
    proptypedet = request.form["proptypedet"]
    property.typeprop_id = \
        Typeproperty.query.with_entities(Typeproperty.id).filter \
            (Typeproperty.proptypedet == proptypedet).one()[0]
    db.session.commit()
    return


def postrental(id, action):
    if action == "edit":
        rental = Rental.query.get(id)
    else:
        rental = Rental()
    rental.propaddr = request.form["propaddr"]
    rental.tenantname = request.form["tenantname"]
    rental.rentpa = request.form["rentpa"]
    rental.arrears = request.form["arrears"]
    rental.startrentdate = request.form["startrentdate"]
    if rental.astdate:
        rental.astdate = request.form["astdate"]
    rental.lastgastest = request.form["lastgastest"]
    rental.note = request.form["note"]
    frequency = request.form["frequency"]
    rental.freq_id = \
        Typefreq.query.with_entities(Typefreq.id).filter(Typefreq.freqdet == frequency).one()[0]
    advarr = request.form["advarr"]
    rental.advarr_id = \
        Typeadvarr.query.with_entities(Typeadvarr.id).filter(Typeadvarr.advarrdet == advarr).one()[0]
    db.session.add(rental)
    db.session.commit()
    id = rental.id

    return redirect('/rental/{}'.format(id))


def postrentobj(id):
    if id > 0:
        rent = Rent.query.get(id)
        agent = Agent.query.filter(Agent.id == rent.agent_id).one_or_none()
    else:
        rent = Rent()
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
    if id < 1:
        rent.rentcode = request.form["rentcode"]
        id = rent.id
    else:
        db.session.commit()

    return redirect('/rentobjpage/{}'.format(id))
