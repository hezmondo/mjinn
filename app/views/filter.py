from flask import Blueprint, render_template,  request
from app.dao.common import get_combodict_filter
from app.dao.filter import get_filters, get_rent_s

filter_bp = Blueprint('filter_bp', __name__)


@filter_bp.route('/load_filter', methods=['GET', 'POST'])
def load_filter():
    # load predefined filters from jstore for filter
    jfilters = get_filters(2)

    return render_template('load_filter.html', jfilters=jfilters)


@filter_bp.route('/filter/<int:filter_id>', methods=['GET', 'POST'])
def filter(filter_id):
    # allows the selection of rent objects using multiple filter inputs for query and pr_query
    action = request.args.get('action', "query", type=str)
    combodict = get_combodict_filter()
    #gather combobox values, with "all" added as an option, in a dictionary
    filterdict, rent_s = get_rent_s(action, filter_id)
    #gather filter values and selected rent objects in two dictionaries

    return render_template('filter.html', action=action, combodict=combodict, filter_id=filter_id,
                           filterdict=filterdict, rent_s=rent_s)
