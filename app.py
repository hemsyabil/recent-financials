from flask import Flask, render_template, jsonify
from access_data import DATA_JSON, filtered_data, total_i_owe_all, name_mapping
import humanize
import re
import pandas as pd

finance_app = Flask(__name__)


# Helper functions
def get_names():
    return list(DATA_JSON.keys())


@finance_app.route('/')
def dashboard():
    total_owed = humanize.intcomma(int(total_i_owe_all))

    return render_template('dashboard.html',
                           title="Financial Dashboard",
                           name="Financial Dashboard",
                           DATA_DICT=DATA_JSON,
                           filtered_data=filtered_data,
                           total_owed=total_owed)


@finance_app.route('/api/financials')
def finance_data():
    return jsonify(DATA_JSON)


@finance_app.route('/<name>')
def personal_dashboard(name):
    sheet_name = name_mapping.get(name)

    if not sheet_name:
        return jsonify({"error": "Record not found"}), 404

    record = DATA_JSON.get(sheet_name, [])
    total_owed = filtered_data[sheet_name]["Total I Owe"]

    df = pd.DataFrame(record)
    table_html = df.to_html(classes='table table-striped table-hover',
                            index=False)

    return render_template('personal-dashboard.html',
                           title="Recent Financials - Dashboard",
                           filtered_data=filtered_data,
                           name=sheet_name,
                           total_owed=total_owed,
                           table=table_html)


@finance_app.route('/api/<name>')
def personal_data(name):
    sheet_name = name_mapping.get(name)

    if not sheet_name:
        return jsonify({"error": "Record not found"}), 404

    record = DATA_JSON.get(sheet_name, [])
    return jsonify(record)


@finance_app.route('/api/names')
def list_names():
    names = get_names()
    return jsonify(names)


if __name__ == "__main__":
    finance_app.run(host='0.0.0.0', port=8080, debug=True)
