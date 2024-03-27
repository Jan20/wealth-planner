import logging
from flask import Flask, g

from application.adapters.controllers.report_controller import report_blueprint
from application.domain.services.commitment_service import CommitmentService
from application.domain.services.report_service import ReportService


def create_app():
    # Create a new Flask application instance.
    app = Flask(__name__)

    # Register the report blueprint to the application.
    app.register_blueprint(report_blueprint)

    # Set the logging level of the application to WARNING.
    app.logger.setLevel(logging.WARNING)

    # Register services with the Flask application context.
    @app.before_request
    def before_request():
        # Check if the 'commitment_service' is not already registered in the application context.
        if 'commitment_service' not in g:
            g.commitment_service = CommitmentService()

        # Check if the 'report_service' is not already registered in the application context.
        if 'report_service' not in g:
            g.report_service = ReportService(g.commitment_service)

    return app


# Entry point of the application.
if __name__ == '__main__':
    # Create the Flask application instance using the create_app() function.
    app: Flask = create_app()

    # Run the application on port 5000 with debugging enabled.
    app.run(port=5000, debug=True)
