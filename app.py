import logging
from blueprints.graph import graphApi
from blueprints.test import testApi
from flask import Flask
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(graphApi)
app.register_blueprint(testApi)

if __name__ == '__main__':
    app.run(debug=True)
