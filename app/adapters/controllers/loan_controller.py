from flask import g, jsonify, Blueprint, send_file, request
from pandas import to_datetime

from app.domain.entities.loan_request import LoanRequest

loan_blueprint = Blueprint('loan', __name__)


@loan_blueprint.route(rule='/loan/forecast', methods=['POST'])
def create_loan_forecast():
    data = request.json

    loan_request = LoanRequest(
        principal=data.get('principal'),
        annual_interest_rate=data.get('annual_interest_rate'),
        start_date=to_datetime(data.get('start_date')),
        end_date=to_datetime(data.get('end_date'))
    )

    try:
        g.loan_forecast_service.create_forecast(loan_request)
        return send_file(path_or_file="files/forecast.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
