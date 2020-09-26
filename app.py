from blueprints.graph import graphApi
from flask import Flask
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


app.register_blueprint(graphApi)

if __name__ == '__main__':
    app.run(debug=True)
