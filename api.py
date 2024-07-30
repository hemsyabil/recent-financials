from app import finance_app
from flask import jsonify
from access_data import DATA_JSON, name_mapping


# Helper functions
def get_names():
    return list(DATA_JSON.keys())


@finance_app.route('/api/financials')
def finance_data():
    return jsonify(DATA_JSON)


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
