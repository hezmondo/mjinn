import sqlalchemy
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from app import db
from app.main import bp
from app.main.get import filteragents, filtercharges, filteremailaccs, filterextrents, filterheadrents, \
    filterincome, filterlandlords, getagent, getcharge, getemailacc, getextrent, \
    getincome, getlandlord, getloan, getloans, getloanstatement, getproperty, getqueryoptions, getqueryparams, \
    getrental, getrentals, getrentalstatement, getrentobj
from app.main.post import postagent, postcharge, postemailacc, postincome, postlandlord, \
    postloan, postproperty, postrental, postrentobj
from app.main.forms import IncomeForm, IncomeAllocForm
from app.models import Agent, Charge, Emailaccount, Income, Jstore, Landlord, Loan, \
    Loan_interest_rate, Loan_trans, Property, Rent, Rental


@bp.route('/agents', methods=['GET', 'POST'])
def agents():
    if request.method == "POST":
        agd = request.form["address"]
        age = request.form["email"]
        agn = request.form["notes"]
    else:
        agd = "Jones"
        age = ""
        agn = ""
    agents = filteragents(agd, age, agn)

    return render_template('agents.html', title='Agent search page', agents=agents)


@bp.route('/agentpage/<int:id>', methods=["GET", "POST"])
@login_required
def agentpage(id):
    if request.method == "POST":
        postagent(id)
    else:
        pass
    agent = getagent(id)

    return render_template('agentpage.html', title='Agent', agent=agent)


@bp.route('/charges', methods=['GET', 'POST'])
def charges():
    rentcode = request.args.get('rentcode', "view", type=str)
    if request.method == "POST":
        rcd = request.form["rentcode"]
        cdt = request.form["chargedetails"]
    else:
        if not rentcode == "view":
            rcd = rentcode
        else:
            rcd = ""
        cdt = ""
    charges = filtercharges(rcd, cdt)

    return render_template('charges.html', title='Charges page', charges=charges)


@bp.route('/chargepage/<int:id>', methods=["GET", "POST"])
@login_required
def chargepage(id):
    if request.method == "POST":
        postcharge(id)
    else:
        pass
    charge, chargedescs = getcharge(id)

    return render_template('chargepage.html', charge=charge, chargedescs=chargedescs)


@bp.route('/deleteitem/<int:id>')
@login_required
def deleteitem(id):
    item = request.args.get('item', "view", type=str)
    if item == "agent":
        agent = Agent.query.get(id)
        db.session.delete(agent)
        db.session.commit()
    elif item == "charge":
        charge = Charge.query.get(id)
        db.session.delete(charge)
        db.session.commit()
    elif item == "emailacc":
        emailacc = Emailaccount.query.get(id)
        db.session.delete(emailacc)
        db.session.commit()
        # return redirect('/emailaccs')
    elif item == "landlord":
        landlord = Landlord.query.get(id)
        if landlord:
            db.session.delete(landlord)
            db.session.commit()
    elif item == "loan":
        delete_loan = Loan.query.get(id)
        # delete_loan_trans = Loan_trans.query.filter(Loan_trans.loan_id == id).all()
        # delete_loan_interest_rate = Loan_interest_rate.query.filter(Loan_interest_rate.loan_id == id).all()
        # db.session.delete(delete_loan_interest_rate)
        # db.session.delete(delete_loan_trans)
        db.session.delete(delete_loan)
        db.session.commit()
    elif item == "rentprop":
        delete_rent = Rent.query.get(id)
        delete_property = Property.query.filter(Property.rent_id == id).first()
        if delete_property:
            db.session.delete(delete_property)
            db.session.delete(delete_rent)
            db.session.commit()

    return redirect(url_for('main.index'))


@bp.route('/emailaccpage/<int:id>', methods=['GET', 'POST'])
@login_required
def emailaccpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postemailacc(id, action)
    else:
        pass
    emailacc = getemailacc(id)

    return render_template('emailaccpage.html', title='Email account', action=action, emailacc=emailacc)


@bp.route('/emailaccs', methods=['GET'])
def emailaccs():
    emailaccs = filteremailaccs()

    return render_template('emailaccs.html', title='Email accounts', emailaccs=emailaccs)


@bp.route('/externalrents', methods=['GET', 'POST'])
def externalrents():
    extrents = filterextrents()

    return render_template('externalrents.html', title='External rents', extrents=extrents)


@bp.route('/extrentpage/<int:id>', methods=["GET"])
@login_required
def extrentpage(id):
    extrent = getextrent(id)

    return render_template('extrentpage.html', title ='External Rent', extrent=extrent)


@bp.route('/headrents', methods=['GET', 'POST'])
def headrents():
    headrents = filterheadrents()

    return render_template('headrents.html', title='Headrents', headrents=headrents)


@bp.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == "POST":
        rcd = request.form["rentcode"]
        pay = request.form["payer"]
        typ = request.form["type"]
        income = filterincome(rcd, pay, typ)
    else:
        income = filterincome("", "", "")

    return render_template('income.html', title='Income', income=income)


@bp.route('/incomeallocpage/<int:id>', methods=['GET', 'POST'])
@login_required
def incomeallocpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        payer = request.form["payer"]
        print(payer)
        rentcodes = request.form.getlist("rentcode")
        print(rentcodes)
        print(request.form)
        # postincome(id, action)
        return redirect(url_for('main.income'))
    else:
        pass
    bankaccs, chargedescs, income, incomeallocs, landlords, paytypedets = getincome(id)

    return render_template('incomeallocpage.html', title='Income allocation', action=action, bankaccs=bankaccs,
                           chargedescs=chargedescs, income=income, incomeallocs=incomeallocs, landlords=landlords,
                           paytypedets=paytypedets
                           )


@bp.route('/incomeformpage/<int:id>', methods=['GET', 'POST'])
@login_required
def incomeformpage(id):
    action = request.args.get('action', "view", type=str)
    incomex = Income.query.get(id)
    incomeform = IncomeForm(obj=incomex)
    bankaccs, chargedescs, income, incomeallocs, landlords, paytypedets = getincome(id)
    incomeform.bankaccount = income.accdesc
    incomeform.typepayment = income.paytypedet
    incomeallocform = IncomeAllocForm()
    for id, income_id, alloc_id, rentcode, total, name, chargedesc in incomeallocs:
        incomeallocform.incall_id = id
        incomeallocform.income_id = income_id
        incomeallocform.alloc_id = alloc_id
        incomeallocform.rentcode = rentcode
        incomeallocform.amount = total
        incomeallocform.name = name
        incomeallocform.inc_type = chargedesc
        incomeform.incomeallocations.append_entry(incomeallocform)
    if request.method == "POST":
        # postincome(id, action)
        for entry in incomeform.incomeallocations.entries:
            print(entry.data)
        # print(request.form)
        return redirect(url_for('income'))
    else:
        pass

    return render_template('incomeformpage.html', title='Income allocation', action=action, bankaccs=bankaccs,
                           chargedescs=chargedescs, landlords=landlords, paytypedets=paytypedets,
                           incomeform=incomeform
                           )


@bp.route('/incomepage/<int:id>', methods=['GET', 'POST'])
@login_required
def incomepage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postincome(id, action)
    else:
        pass
    bankaccs, chargedescs, income, incomeallocs, landlords, paytypedets = getincome(id)

    return render_template('incomepage.html', title='Income', action=action, bankaccs=bankaccs,
                           chargedescs=chargedescs, income=income, incomeallocs=incomeallocs, landlords=landlords,
                           paytypedets=paytypedets
                           )


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    qrentobjs, agentdetails, propaddr, rentcode, source, tenantname = getqueryparams("basic")

    return render_template('homepage.html', title='Home page', agentdetails=agentdetails, jname="QALL",
                           propaddr=propaddr, rentcode=rentcode, qrentobjs=qrentobjs,
                           source=source, tenantname=tenantname)


@bp.route('/landlordpage/<int:id>', methods=['GET', 'POST'])
@login_required
def landlordpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postlandlord(id, action)
    else:
        pass
    landlord, managers, emailaccs, bankaccs = getlandlord(id)

    return render_template('landlordpage.html', title='Landlord', action=action, landlord=landlord,
                           bankaccs=bankaccs, managers=managers, emailaccs=emailaccs)


@bp.route('/landlords', methods=['GET'])
def landlords():
    landlords = filterlandlords()

    return render_template('landlords.html', title='Landlords', landlords=landlords)


@bp.route('/loadquery', methods=['GET', 'POST'])
def loadquery():
    if request.method == "POST":
        jqname = request.form["jqname"]
        return redirect("/queries/?name={}".format(jqname))
    else:
        pass
    jqueries = [value for (value,) in Jstore.query.with_entities(Jstore.name).all()]

    return render_template('loadquery.html', title='Load saved query', jqueries=jqueries)


@bp.route('/loanpage/<int:id>', methods=['GET', 'POST'])
@login_required
def loanpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postloan(id)
    else:
        pass
    loan, advarrdets, freqdets = getloan(id)

    return render_template('loanpage.html', title='Loan', action=action, loan=loan,
                           advarrdets=advarrdets, freqdets=freqdets)


@bp.route('/loans', methods=['GET', 'POST'])
def loans():
    loans, loansum = getloans()

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
        loanstatement = getloanstatement()
        loan = Loan.query.get(id)
        loancode = loan.code

        return render_template('loanstatement.html', title='Loan statement', loanstatement=loanstatement,
                               loancode=loancode, checksums=checksums)


@bp.route('/money', methods=['GET', 'POST'])
def money():
    money = None

    return render_template('money.html', title='Money', money=money)


@bp.route('/payrequests', methods=['GET', 'POST'])
@login_required
def payrequests():
    payrequests = None

    return render_template('payrequests.html', title='Payrequests', payrequests=payrequests)


@bp.route('/properties', methods=['GET', 'POST'])
@login_required
def properties():
    properties = None

    return render_template('properties.html', title='Properties', properties=properties)


@bp.route('/propertypage/<int:id>', methods=["GET", "POST"])
@login_required
def propertypage(id):
    if request.method == "POST":
        postproperty(id)
    else:
        pass
    property, proptypedets = getproperty(id)

    return render_template('propertypage.html', title='Property', property=property, proptypedets=proptypedets)


@bp.route('/queries/', methods=['GET', 'POST'])
def queries():
    jname = request.args.get('name', "basic", type=str)
    actypes, floads, landlords, salegrades, statuses, tenures, options, prdeliveries = getqueryoptions()

    qrentobjs, actype, agentdetails, arrears, enddate, landlord, prdelivery, propaddr, rentcode, \
    rentpa, rentperiods, runsize, salegrade, savename, source, status, tenantname, tenure = getqueryparams(jname)

    if savename and savename != "":
        jname = savename

    return render_template('homepage.html', title='Home page', action='advanced', actype=actype, actypes=actypes,
                           agentdetails=agentdetails, arrears=arrears, enddate=enddate, floads=floads,
                           jname=jname, landlord=landlord, landlords=landlords, options=options, prdelivery=prdelivery,
                           prdeliveries=prdeliveries, propaddr=propaddr, rentcode=rentcode, qrentobjs=qrentobjs,
                           rentpa=rentpa, runsize=runsize, salegrade=salegrade, salegrades=salegrades, source=source,
                           status=status, statuses=statuses, tenantname=tenantname, tenure=tenure, tenures=tenures)


@bp.route('/rentals', methods=['GET', 'POST'])
def rentals():
    rentals, rentsum = getrentals()

    return render_template('rentals.html', title='Rentals page', rentals=rentals, rentsum=rentsum)


@bp.route('/rentalpage/<int:id>', methods=['GET', 'POST'])
@login_required
def rentalpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postrental(id)
    else:
        pass
    rental, advarrdets, freqdets = getrental(id)

    return render_template('rentalpage.html', title='Rental', action=action, rental=rental,
                           advarrdets=advarrdets, freqdets=freqdets)


@bp.route('/rentalstatementpage/<int:id>', methods=["GET", "POST"])
@login_required
def rentalstatementpage(id):
    if request.method == "POST":
        pass
    else:
        db.session.execute(sqlalchemy.text("CALL pop_rental_statement(:x)"), params={"x": id})
        db.session.commit()
        rentalstatement = getrentalstatement()
        print("rentalstate")
        print(rentalstatement)

        return render_template('rentalstatement.html', title='Rental statement', rentalstatement=rentalstatement)


@bp.route('/rentobjpage/<int:id>', methods=['GET', 'POST'])
@login_required
def rentobjpage(id):
    action = request.args.get('action', "view", type=str)
    if request.method == "POST":
        postrentobj(id)
    else:
        pass
    rentobj, actypedets, advarrdets, deedcodes, freqdets, landlords, mailtodets, properties, \
            salegradedets, statusdets, tenuredets, totcharges = getrentobj(id)

    return render_template('rentobjpage.html', action=action, title=action, rentobj=rentobj,
                       actypedets=actypedets, advarrdets=advarrdets, deedcodes=deedcodes, freqdets=freqdets,
                       landlords=landlords, mailtodets=mailtodets, properties=properties,
                       salegradedets=salegradedets, statusdets=statusdets, tenuredets=tenuredets, totcharges=totcharges)


@bp.route('/utilities', methods=['GET'])
def utilities():

    return render_template('utilities.html', title='utilities')