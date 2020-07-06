import sqlalchemy
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from app import db
from app.main import bp
from app.main.get import get_agent, get_agents, get_charge, get_charges, get_emailaccount, get_emailaccounts, \
    get_externalrent, get_headrents, get_incomeobject, \
    get_incomeitems, get_incomeoptions, get_incomeobjectoptions, \
    get_landlord, get_landlords, get_loan, get_loan_options, get_loans, get_loanstatement, get_moneyaccount, \
    get_moneydets, get_moneyitem, get_moneyitems, get_money_options, \
    get_property, get_rental, getrentals, get_rentalstatement, getrentobj, get_rentobjects
from app.main.post import post_agent, post_charge, post_emailaccount, post_incomeobject, post_landlord, \
    post_loan, post_moneyaccount, post_moneyitem, post_property, post_rental, postrentobj
from app.models import Agent, Charge, Emailaccount, Income, Incomealloc, Jstore, Landlord, Loan, Money_account, \
    Money_category, Money_item, Loan_interest_rate, Loan_trans, Property, Rent, Rental


@bp.route('/agents', methods=['GET', 'POST'])
def agents():
    agents = get_agents()

    return render_template('agents.html', agents=agents)


@bp.route('/agent/<int:id>', methods=["GET", "POST"])
@login_required
def agent(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_agent(id, action)
        return redirect('/agent/{}'.format(id))
    agent = get_agent(id)

    return render_template('agent.html', action=action, agent=agent)


@bp.route('/charges', methods=['GET', 'POST'])
def charges():
    rentcode = request.args.get('rentcode', "", type=str)
    charges = get_charges(rentcode)

    return render_template('charges.html', charges=charges)


@bp.route('/charge/<int:id>', methods=["GET", "POST"])
@login_required
def charge(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_charge(id, action)
    charge, chargedescs = get_charge(id)

    return render_template('charge.html', action=action, charge=charge, chargedescs=chargedescs)


@bp.route('/delete_item/<int:id>')
@login_required
def delete_item(id):
    item = request.args.get('item', "view", type=str)
    if item == "agent":
        d_agent = Agent.query.get(id)
        db.session.delete(d_agent)
        db.session.commit()
        return redirect('/agents')
    elif item == "bankitem":
        d_bankitem = Money_item.query.get(id)
        if d_bankitem:
            db.session.delete(d_bankitem)
            db.session.commit()
            return redirect('/money')
    elif item == "charge":
        d_charge = Charge.query.get(id)
        if d_charge:
            db.session.delete(d_charge)
            db.session.commit()
            return redirect('/charges')
    elif item == "emailacc":
        d_emailacc = Emailaccount.query.get(id)
        if d_emailacc:
            db.session.delete(d_emailacc)
            db.session.commit()
            return redirect('/emailaccs')
    elif item == "incomealloc":
        d_alloc = Incomealloc.query.get(id)
        if d_alloc:
            db.session.delete(d_alloc)
            db.session.commit()
            return redirect('/income')
    elif item == "landlord":
        d_landlord = Landlord.query.get(id)
        if d_landlord:
            db.session.delete(d_landlord)
            db.session.commit()
            return redirect('/landlords')
    elif item == "loan":
        d_loan = Loan.query.get(id)
        # delete_loan_trans = Loan_trans.query.filter(Loan_trans.loan_id == id).all()
        # delete_loan_interest_rate = Loan_interest_rate.query.filter(Loan_interest_rate.loan_id == id).all()
        # db.session.delete(delete_loan_interest_rate)
        # db.session.delete(delete_loan_trans)
        db.session.delete(d_loan)
        db.session.commit()
        return redirect('/loans')
    elif item == "moneyacc":
        d_moneyacc = Money_account.query.get(id)
        if d_moneyacc:
            db.session.delete(d_moneyacc)
            db.session.commit()
            return redirect('/money_accounts')
    elif item == "rentprop":
        d_rent = Rent.query.get(id)
        d_property = Property.query.filter(Property.rent_id == id).first()
        if d_property:
            db.session.delete(d_property)
        db.session.delete(d_rent)
        db.session.commit()
        return redirect(url_for('main.index'))


@bp.route('/email_accounts', methods=['GET'])
def email_accounts():
    emailaccs = get_emailaccounts()

    return render_template('email_accounts.html', emailaccs=emailaccs)


@bp.route('/email_account/<int:id>', methods=['GET', 'POST'])
@login_required
def email_account(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_emailaccount(id, action)
    emailacc = get_emailaccount(id)

    return render_template('email_account.html', action=action, emailacc=emailacc)


@bp.route('/external_rents', methods=['GET', 'POST'])
def external_rents():
    agentdetails, propaddr, rentcode, source, tenantname, rentprops = get_rentobjects("external", "queryall")

    return render_template('external_rents.html', agentdetails=agentdetails, propaddr=propaddr, rentcode=rentcode,
                           source=source, tenantname=tenantname, rentprops=rentprops)


@bp.route('/externalrentpage/<int:id>', methods=["GET"])
@login_required
def externalrentpage(id):
    externalrent = get_externalrent(id)

    return render_template('external_rent.html', externalrent=externalrent)


@bp.route('/headrents', methods=['GET', 'POST'])
def headrents():
    headrents, statuses = get_headrents()

    return render_template('headrents.html', headrents=headrents, statuses=statuses)


@bp.route('/income', methods=['GET', 'POST'])
def income():
    incomeitems = get_incomeitems()
    bankaccs, paytypes = get_incomeoptions()

    return render_template('income.html', bankaccs=bankaccs, paytypes=paytypes, incomeitems=incomeitems)


@bp.route('/income_object/<int:id>', methods=['GET', 'POST'])
@login_required
def income_object(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_incomeobject(id, action)

    bankaccs, chargedescs, landlords, paytypes = get_incomeobjectoptions()
    income, incomeallocs = get_incomeobject(id)

    return render_template('income_object.html', action=action, bankaccs=bankaccs, chargedescs=chargedescs,
                           income=income, incomeallocs=incomeallocs, landlords=landlords, paytypes=paytypes)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    agentdetails, propaddr, rentcode, source, tenantname, rentprops = get_rentobjects("basic", "queryall")

    return render_template('homepage.html', action="basic", agentdetails=agentdetails, jname="queryall",
                           propaddr=propaddr, rentcode=rentcode, source=source, tenantname=tenantname,
                           rentprops=rentprops)


@bp.route('/landlords', methods=['GET'])
def landlords():
    landlords = get_landlords()

    return render_template('landlords.html', landlords=landlords)


@bp.route('/landlord/<int:id>', methods=['GET', 'POST'])
@login_required
def landlord(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id_ = post_landlord(id, action)
        return redirect('/landlord/{}?action=view'.format(id_))
    else:
        pass
    landlord, managers, emailaccs, bankaccs = get_landlord(id)

    return render_template('landlord.html', title='Landlord', action=action, landlord=landlord,
                           bankaccs=bankaccs, managers=managers, emailaccs=emailaccs)


@bp.route('/loadquery', methods=['GET', 'POST'])
def loadquery():
    if request.method == "POST":
        jqname = request.form["jqname"]
        return redirect("/queries/?name={}".format(jqname))
    else:
        pass
    jqueries = [value for (value,) in Jstore.query.with_entities(Jstore.name).all()]

    return render_template('loadquery.html', jqueries=jqueries)


@bp.route('/loan/<int:id>', methods=['GET', 'POST'])
@login_required
def loan(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_loan(id, action)
    loan = get_loan(id)
    advarrdets, freqdets = get_loan_options()

    return render_template('loan.html', title='Loan', action=action, loan=loan,
                           advarrdets=advarrdets, freqdets=freqdets)


@bp.route('/loans', methods=['GET', 'POST'])
def loans():
    loans, loansum = get_loans()

    return render_template('loans.html', title='Loans page', loans=loans, loansum=loansum)


@bp.route('/loanstatementpage/<int:id>', methods=["GET", "POST"])
@login_required
def loanstatementpage(id):
    if request.method == "POST":
        pass
    else:
        rproxy = db.session.execute(sqlalchemy.text("CALL pop_loan_statement(:x)"), params={"x": id})
        checksums = rproxy.fetchall()
        db.session.commit()
        loanstatement = get_loanstatement()
        loan = Loan.query.get(id)
        loancode = loan.code

        return render_template('loanstatement.html', title='Loan statement', loanstatement=loanstatement,
                               loancode=loancode, checksums=checksums)


@bp.route('/money', methods=['GET', 'POST'])
def money():
    moneydets, accsums = get_moneydets()

    return render_template('money.html', moneydets=moneydets, accsums=accsums)


@bp.route('/money_accounts', methods=['GET', 'POST'])
def money_accounts():
    moneyaccs = Money_account.query.all()

    return render_template('money_accounts.html', moneyaccs=moneyaccs)


@bp.route('/money_account/<int:id>', methods=['GET', 'POST'])
@login_required
def money_account(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id_ = post_moneyaccount(id, action)
        return redirect('/money_account/{}?action=view'.format(id_))
    moneyacc = get_moneyaccount(id)

    return render_template('money_account.html', action=action, moneyacc=moneyacc)


@bp.route('/money_deduce/<int:id>', methods=['GET', 'POST'])
def money_deduce(id):
    action = request.args.get('action', "view", type=str)
    if action == "X":
        return redirect('/income_object/{}'.format(id))
    else:
        return redirect('/money_item/{}'.format(id))


@bp.route('/money_items/<int:id>', methods=["GET", "POST"])
@login_required
def money_items(id):
    action = request.args.get('action', "account", type=str)
    bankaccs, cats, cleareds = get_money_options()
    accsums, moneyitems, values = get_moneyitems(id, action)

    return render_template('money_items.html', action=action, moneyitems=moneyitems, values=values,
                           bankaccs=bankaccs, accsums=accsums, cats=cats, cleareds=cleareds)


@bp.route('/money_item/<int:id>', methods=['GET', 'POST'])
def money_item(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id_ = post_moneyitem(id, action)
        return redirect('/money_item/{}?action=view'.format(id_))

    else:
        pass
    bankaccs, cats, cleareds = get_money_options()
    moneyitem = get_moneyitem(id)

    return render_template('money_item.html', action=action, moneyitem=moneyitem, bankaccs=bankaccs,
                           cats=cats, cleareds=cleareds)


@bp.route('/payrequests', methods=['GET', 'POST'])
@login_required
def payrequests():
    payrequests = None

    return render_template('payrequests.html', payrequests=payrequests)


@bp.route('/properties', methods=['GET', 'POST'])
# @login_required
def properties():
    properties = None

    return render_template('properties.html', properties=properties)


@bp.route('/property/<int:id>', methods=["GET", "POST"])
# @login_required
def property(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_property(id, action)
    property, proptypedets = get_property(id)

    return render_template('property.html', action=action, property=property, proptypedets=proptypedets)


@bp.route('/queries/', methods=['GET', 'POST'])
def queries():
    action = request.args.get('action', "view", type=str)
    name = request.args.get('name', "queryall", type=str)
    actypes, floads, landlords, options, prdeliveries, salegrades, statuses, tenures, \
    actype, agentdetails, arrears, enddate, jname, landlord, prdelivery, propaddr, rentcode, rentpa, rentperiods, \
    runsize, salegrade, source, status, tenantname, tenure, rentprops = get_rentobjects(action, name)

    return render_template('homepage.html', title='Home page', action=action, actypes=actypes, floads=floads,
                           landlords=landlords, options=options, prdeliveries=prdeliveries, salegrades=salegrades,
                           statuses=statuses, tenures=tenures, actype=actype, agentdetails=agentdetails,
                           arrears=arrears, enddate=enddate, jname=jname, landlord=landlord, prdelivery=prdelivery,
                           propaddr=propaddr, rentcode=rentcode, rentpa=rentpa, rentperiods=rentperiods,
                           runsize=runsize, salegrade=salegrade, source=source, status=status,
                           tenantname=tenantname, tenure=tenure, rentprops=rentprops)


@bp.route('/rentals', methods=['GET', 'POST'])
def rentals():
    rentals, rentsum = getrentals()

    return render_template('rentals.html', rentals=rentals, rentsum=rentsum)


@bp.route('/rental/<int:id>', methods=['GET', 'POST'])
# @login_required
def rental(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        id = post_rental(id, action)
    rental, advarrdets, freqdets = get_rental(id)

    return render_template('rental.html', title='Rental', action=action, rental=rental,
                           advarrdets=advarrdets, freqdets=freqdets)


@bp.route('/rentalstatement/<int:id>', methods=["GET", "POST"])
# @login_required
def rentalstatement(id):
    db.session.execute(sqlalchemy.text("CALL pop_rental_statement(:x)"), params={"x": id})
    db.session.commit()
    rentalstatem = get_rentalstatement()
    print("rentalstatem")
    print(rentalstatem)

    return render_template('rentalstatement.html', title='Rental statement', rentalstatem=rentalstatem)


@bp.route('/rentobjpage/<int:id>', methods=['GET', 'POST'])
# @login_required
def rentobjpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postrentobj(id)
    else:
        pass
    rentobj, actypedets, advarrdets, deedcodes, freqdets, landlords, mailtodets, properties, \
            salegradedets, statusdets, tenuredets, totcharges = getrentobj(id)

    return render_template('rent_object.html', action=action, title=action, rentobj=rentobj,
                       actypedets=actypedets, advarrdets=advarrdets, deedcodes=deedcodes, freqdets=freqdets,
                       landlords=landlords, mailtodets=mailtodets, properties=properties,
                       salegradedets=salegradedets, statusdets=statusdets, tenuredets=tenuredets, totcharges=totcharges)


@bp.route('/utilities', methods=['GET'])
def utilities():

    return render_template('utilities.html', title='utilities')