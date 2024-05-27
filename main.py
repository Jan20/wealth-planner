import locale
import logging

from flask import Flask, g

from app.adapters.controllers.loan_controller import loan_blueprint
from app.adapters.controllers.pension_controller import pension_blueprint
from app.adapters.controllers.portfolio_controller import portfolio_blueprint
from app.adapters.controllers.rent_controller import rent_blueprint
from app.domain.services.loan.loan_forecast_service import LoanForecastService
from app.domain.services.loan.loan_service import LoanService
from app.domain.services.pension.pension_forecast_service import PensionForecastService
from app.domain.services.pension.pension_service import PensionService
from app.domain.services.portfolio.portfolio_document_service import PortfolioForecastService
from app.domain.services.portfolio.portfolio_service import PortfolioService
from app.domain.services.rent.rent_forecast_service import RentForecastService
from app.domain.services.rent.rent_service import RentService

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'de_DE.UTF-8')


def create_app():

    app: Flask = Flask(__name__)
    app.logger.setLevel(logging.WARNING)

    app = register_blueprints(app)

    @app.before_request
    def before_request():
        if 'pension_service' not in g:
            g.pension_service = PensionService()

        if 'pension_forecast_service' not in g:
            g.pension_forecast_service = PensionForecastService(g.pension_service)

        if 'rent_service' not in g:
            g.rent_service = RentService()

        if 'rent_forecast_service' not in g:
            g.rent_forecast_service = RentForecastService(g.rent_service)

        if 'loan_service' not in g:
            g.loan_service = LoanService()

        if 'loan_forecast_service' not in g:
            g.loan_forecast_service = LoanForecastService(g.loan_service)

        if 'portfolio_service' not in g:
            g.portfolio_service = PortfolioService()

        if 'portfolio_forecast_service' not in g:
            g.portfolio_forecast_service = PortfolioForecastService(g.portfolio_service)

    return app


def register_blueprints(app: Flask) -> Flask:
    blueprints = [
        loan_blueprint,
        rent_blueprint,
        portfolio_blueprint,
        pension_blueprint
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000)
