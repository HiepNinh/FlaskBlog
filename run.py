from flask import Flask
from config import Config
from databases import initialize_database
from flaskblog import regist_blueprints
from extensions import initialize_utils
from flask_restful import Api
from api.routes import initialize_routes


app = Flask(__name__)
app.config.from_object(Config)

initialize_database(app)
initialize_utils(app)
regist_blueprints(app)

api = Api(app)
initialize_routes(api)


if __name__ == '__main__':
    app.run(debug=True)