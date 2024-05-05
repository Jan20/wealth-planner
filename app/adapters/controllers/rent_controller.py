from flask import g, jsonify, Blueprint, send_file, request
from pandas import to_datetime

from app.domain.entities.rent_request import RentRequest

rent_blueprint = Blueprint('rent', __name__)


@rent_blueprint.route(rule='/rent/forecast', methods=['POST'])
def create_rent_document():
    data = request.json

    rent_request = RentRequest(
        monthly_rent=data.get('monthly_rent'),
        annual_increase=data.get('annual_increase'),
        start_date=to_datetime(data.get('start_date')),
        end_date=to_datetime(data.get('end_date'))
    )

    try:
        g.rent_forecast_service.create_forecast(rent_request)
        return send_file(path_or_file="files/forecast.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
