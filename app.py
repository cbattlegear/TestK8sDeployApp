# Set up the libraries for the configuration and base web interfaces
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
import pyodbc

import os
import configparser
import json

# Load the variables from the .env file
load_dotenv()

# Create the Flask-RESTful Application
app = Flask(__name__)
api = Api(app)

# Create connection to Azure SQL Database using the config.ini file values
server_name = os.getenv('SQL_SERVER_ENDPOINT')
database_name = os.getenv('SQL_SERVER_DATABASE')
user_name = os.getenv('SQL_SERVER_USERNAME')
password = os.getenv('SQL_SERVER_PASSWORD')

config = configparser.ConfigParser()
# Create connection to Azure SQL Database using the config.ini file values
ServerName = config.get('Connection', 'SQL_SERVER_ENDPOINT')
DatabaseName = config.get('Connection', 'SQL_SERVER_DATABASE')
UserName = config.get('Connection', 'SQL_SERVER_USERNAME')
PasswordValue = config.get('Connection', 'SQL_SERVER_PASSWORD')

# Connect to Azure SQL Database using the pyodbc package
# Note: You may need to install the ODBC driver if it is not already there. You can find that at:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#version-17
connection = pyodbc.connect(f'Driver=ODBC Driver 17 for SQL Server;Server={ServerName};Database={DatabaseName};uid={UserName};pwd={PasswordValue}')

# Create the SQL query to run against the database
def query_db():
    cursor = connection.cursor()
    cursor.execute("SELECT TOP (10) [ProductID], [Name], [Description] FROM [SalesLT].[vProductAndDescription] WHERE Culture = 'EN' FOR JSON AUTO;")
    result = cursor.fetchone()
    cursor.close()
    return result

# Create the class that will be used to return the data from the API
class Products(Resource):
    def get(self):
        result = query_db()
        json_result = {} if (result == None) else json.loads(result[0])     
        return json_result, 200

# Set the API endpoint to the Products class
api.add_resource(Products, '/products')

# Start App on default Flask port 5000
if __name__ == "__main__":
    app.run(debug=True)