from flask import Blueprint, render_template,  request
from flask_login import login_required
from app.dao.rent import get_rent_addrs
from app.dao.form_letter import get_fm_letters, get_form_letters
from app.main.mail import writeMail, writeMail_xray

mail_bp = Blueprint('mail_bp', __name__)


@mail_bp.route('/mail_dialog/<int:rent_id>', methods=["GET", "POST"])
@login_required
def mail_dialog(rent_id):
    action = request.args.get('action', "all", type=str)
    form_letters = get_form_letters(action)
    rent_addrs = get_rent_addrs(rent_id)
    return render_template('mail_dialog.html', action=action, form_letters=form_letters, rent_addrs=rent_addrs)


@mail_bp.route('/mail_dialog_x/<int:rent_id>', methods=["GET", "POST"])
@login_required
def mail_dialog_x(rent_id):
    action = request.args.get('action', "all", type=str)
    fm_letters = get_fm_letters(action)
    rent_addrs = get_rent_addrs(rent_id)
    return render_template('mail_dialog.html', action=action, form_letters=fm_letters, rent_addrs=rent_addrs)


@mail_bp.route('/mail_edit/<int:form_letter_id>', methods=["GET", "POST"])
@login_required
def mail_edit(form_letter_id):
    method = request.args.get('method', "email", type=str)
    if request.method == "POST":
        form_letter_id = form_letter_id
        income_id = request.form.get('income_id') or 0
        rent_id = request.form.get('rent_id')
        block, leasedata, rent, subject, doctype, dcode = writeMail(rent_id, form_letter_id, income_id)
        mailaddr = request.form.get('mailaddr')
        summary = dcode + "-" + method + "-" + mailaddr[0:25]
        mailaddr = mailaddr.split(", ")
        return render_template('mergedocs/LTS.html', block=block, doctype=doctype, summary=summary,
                               leasedata=leasedata, mailaddr=mailaddr, method=method, rent=rent, subject=subject)


@mail_bp.route('/mail_edit_x/<int:fm_letter_id>', methods=["GET", "POST"])
@login_required
def mail_edit_x(fm_letter_id):
    method = request.args.get('method', "email", type=str)
    if request.method == "POST":
        fm_letter_id = fm_letter_id
        income_id = request.form.get('income_id') or 0
        rent_id = request.form.get('rent_id')
        doctype, code, leasedata, rent, variables = writeMail_xray(rent_id, fm_letter_id, income_id)
        mailaddr = request.form.get('mailaddr')
        mailaddr = mailaddr.split(", ")
        summary = f"{method}-{code}-to-{rent.email}"
        email_to = rent.email
        email_subject = f"Re: {rent.propaddr}"
        return render_template(f"mergedocs/{code}.html", doctype=doctype, email_subject=email_subject,
                               email_to=email_to, leasedata=leasedata, mailaddr=mailaddr, method=method, rent=rent,
                               summary=summary, variables=variables)
