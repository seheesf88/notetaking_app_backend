from flask import Flask
from resources.postings import postings_api

from flask_cors import CORS

import models
import config



app = Flask(__name__)
app.secret_key = config.SECRET_KEY


CORS(postings_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(postings_api, url_prefix='/api/v1')

@app.route('/')
def index():
    return 'Hi, NeuroPace'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
