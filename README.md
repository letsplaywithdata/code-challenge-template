# Code Challenge Template

Database - Postgresql

Server - Python Flask Server

Pre-requisites:

    1. Install Postgresql database or create a PostgreSQL database in AWS
    2. Install all the python package dependencies using the below command in the root folder:
        pip install -r requirements.txt

Tables Schema:

    1. class WeatherData(Base):
    __tablename__ = 'weather_data'

    station_id = Column(String(20), primary_key=True)
    date = Column(Date, primary_key=True)
    max_temp = Column(Numeric)
    min_temp = Column(Numeric)
    precipitation = Column(Numeric)


    2. class WeatherLogs(Base):
    __tablename__ = 'weather_logs'

    start_time = Column(Date)
    end_time = Column(Date)
    no_of_records = Column(Integer)
    station_id = Column(String(20), primary_key=True)


    3. class WeatherStats(Base):
    __tablename__ = 'weather_stats'

    station_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    avg_min_temp = Column(Numeric)
    avg_max_temp = Column(Numeric)
    avg_precipitation = Column(Numeric)

Folder Structure:

    code-challenge-template
        i) src
            a) api - directory containing 
                1) server.py : Python file resposible to launch the Flask server and expose the required end points
                2) static - directory containing "swagger.yaml" that provides automatic documentation of API.
            b) Config - directory containing config.json - Configuration file which holds AWS postgresql database config
            c) data_analysis - directory containing: 
                1) fetch_data_filters.py - Python file containing methods to get weather data and weather stats as per 
                    query filters
                2) weather_stats.py - Python file containing method to calculate_weather_stats as per requirements
            d) database - directory containing: 
                1) connection.py : Python file that helps in creating a connection to database using config.json
                2) create_tables.py : Python file that creates the tables required for this problem
                3) drop_tables.py : Python file helps in dropping tables 
            e) ingestion - directory containing: 
                1) fetch_data.py : Python file to fetch data from input folder wx_data using multi-processing for 
                    faster uploads and shows progress bar for upload
                2) ingest_data.py : Python file to Uploads weather data to the database using bulk insert for 
                    faster performance.
            f) tests - directory containing: 
                1) unit_tests.py : Python file to run unit tests for api using pytest library
            g) utils - directory containing: 
                1) adapter_method.py : defines and registers three adapters for NumPy float64 and int64 types, and 
                    Python float type, to be used with the PostgreSQL database adapter.
            h) run.py - Main python file that is responsible for the application flow
            
        ii) wx_data - Input folder with weather station data files
        iii) yld_data - Input folder with yield data files
        iv) requirements.txt - File with python dependencies
        v) README.md
    

Application Flow:

    1. To install required dependencies please run the below command
        pip install - r requirements.txt
    2. To launch the application run the below command in the src folder
        python run.py
    3. The application can be launched in two modes i.e., only Flask server mode where we can make the GET requests and the second mode in which the data is injected into database initially and then the flask server is launched.
    4. In order to run the flask server alone enter 1, inorder to inject and run the flask server enter 2.
    5. Before running the flask server or performing data injection we establish databse connection.
    6. The database configurations are present inside config.json file. Please configure the values according to the local setup.
    7. In case of data injection we are following the below steps:
        a. Drop the existing tables in the database
        b. Create required tables
        c. Read data from input folder which is present in the same directory as that of src folder. The input folders should be named as wx_data.
        d. Once all the data is read, we inject these data into the database.
    8. Once we are done with the data injection step we start the flask server (In case we choose 1 in the initial launch option it runs the flask server directly without the aobve data injection steps).
    9. The flask server will be launched in host = 0.0.0.0 (127.0.0.1) and port = 8081. Incase these values should be changed then please refer to the app.run statement in server.py.
    (Don't use the default URL output shown in the terminal, use the api calls mentioned below)
    10. The flask server exposes two API endpoints
        a. /api/weather
            - Query Params (Optional for filter purpose):
                i) station_id :- weather station id
                ii) date :- Record date
                iii) limit :- Number of records to be returned for pagenation purpose
                iv) offset :- Position/index to start records from for pagenation purpose. We return limit number of records from the given offset.
            - In case both station_id and date are provided in the query params then there is no use of limit and offset as only one record will be returned.
            - Example API Requests with different filter options:
                i) http://localhost:8081/api/weather
                ii) http://localhost:8081/api/weather?offset=1&limit=100&date=19920101
                iii) http://localhost:8081/api/weather?offset=1&limit=100&station_id=USC00110072
                iv) http://localhost:8081/api/weather?date=19920101&station_id=USC00110072
                v) http://localhost:8081/api/weather?station_id=USC00110072
        
        b. /api/weather/stats
            - Query Params (Optional for filter purpose):
                i) station_id :- weather station id
                ii) year :- Record year
                iii) limit :- Number of records to be returned for pagenation purpose
                iv) offset :- Position/index to start records from for pagenation purpose. We return limit number of records from the given offset.
            - In case both station_id and year are provided in the query params then there is no use of limit and offset as only one record will be returned.
            - Example API Requests with different filter options:
                i) http://localhost:8081/api/weather/stats
                ii) http://localhost:8081/api/weather/stats?offset=1&limit=100&date=2012
                iii) http://localhost:8081/api/weather/stats?offset=1000&limit=500&station_id=USC00110072
                iv) http://localhost:8081/api/weather/stats?date=1992&station_id=USC00110072
                v) http://localhost:8081/api/weather/stats?station_id=USC00110072

    11. With the help of Swagger, we expose the documentation for API at:
            /api/docs
            - Provides the same query parameters as required by :
            /api/weather and
            /api/weather/stats

    12. _NOTE_ : Implementation of reading data from folder (fetch_data.py) has been done with help of cpu threads. 
            The current value has been set at '4' which can be changed if required based on device.
    
    13. Extra Credit - Deployment has been added to 'answers' directory