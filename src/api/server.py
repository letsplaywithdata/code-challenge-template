from flask import Flask, request, jsonify
from data_analysis import fetch_data_filters
from flask_swagger_ui import get_swaggerui_blueprint


def start_server(conn):
    app = Flask(__name__)
    # Swagger UI config
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.yaml'  # Swagger UI YAML file
    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={
        'app_name': "Weather API"
    })
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Method to perform @Get(/api/weather)
    @app.route('/api/weather', methods=['GET'])
    def get_weather_data():
        # Read respective filter options
        args = request.args
        station_id = args.get("station_id", "", type=str)
        date_val = args.get("date", "", type=str)
        page_id = args.get("offset", 1, type=int)
        page_size = args.get("limit", 1000, type=int)
        # Get data from database
        records = fetch_data_filters.get_weather_data(conn,station_id, date_val, page_id, page_size)
        return jsonify(records)

    # Method to perform @Get(/api/weather/stats)
    @app.route('/api/weather/stats', methods=['GET'])
    def get_weather_stats():
        # Read respective filter options
        args = request.args
        station_id = args.get("station_id", "", type=str)
        year_val = args.get("year", 0, type=int)
        page_id = args.get("offset", 1, type=int)
        page_size = args.get("limit", 500, type=int)
        # Get data from database
        records = fetch_data_filters.get_weather_stats(conn,station_id, year_val, page_id, page_size)
        return jsonify(records)

    # Start server on 0.0.0.0 host and 8081 port
    app.run(host='0.0.0.0', port=8081)
