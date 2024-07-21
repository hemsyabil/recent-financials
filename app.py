from flask import Flask, render_template, jsonify
from access_data import DATA_JSON, filtered_data, total_i_owe_all
import humanize

finance_app = Flask(__name__)


@finance_app.route('/')
def dashboard():
    total_owed = humanize.intcomma(int(total_i_owe_all))

    return render_template('index.html',
                           title="Recent Financials - Dashboard",
                           name="dashboard",
                           DATA_DICT=DATA_JSON,
                           filtered_data=filtered_data,
                           total_owed=total_owed)


@finance_app.route('/api/financials')
def finance_data():
    return jsonify(DATA_JSON)


if __name__ == "__main__":
    finance_app.run(host='0.0.0.0', port=8080, debug=True)
