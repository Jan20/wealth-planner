from flask import g, jsonify, Blueprint, send_file

report_blueprint = Blueprint('report', __name__)


@report_blueprint.route(rule='/report', methods=['GET'])
def generate_financial_report():
    try:
        # Generate the financial report using the report service
        g.report_service.generate_report()

        # Send the generated report file as a response
        return send_file(path_or_file="report.pdf", as_attachment=True)

    except Exception as e:
        # Handle exceptions gracefully and return an error response
        return jsonify({'error': str(e)})
