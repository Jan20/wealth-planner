from flask import g, jsonify, Blueprint, send_file, request
from pandas import to_datetime

from app.domain.entities.portfolio_request import PortfolioRequest

portfolio_blueprint = Blueprint('portfolio', __name__)


@portfolio_blueprint.route(rule='/portfolio/forecast', methods=['POST'])
def create_rent_document():
    data = request.json

    portfolio_request = PortfolioRequest(
        initial_portfolio=data.get('initial_portfolio'),
        yearly_return=data.get('yearly_return'),
        yearly_contribution=data.get('yearly_contribution'),
        start_date=to_datetime(data.get('start_date')),
        end_date=to_datetime(data.get('end_date'))
    )

    try:
        g.portfolio_forecast_service.create_forecast(portfolio_request)
        return send_file(path_or_file="files/forecast.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
