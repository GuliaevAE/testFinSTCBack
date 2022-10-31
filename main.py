from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/') 
def index(): 
    return "WELCOME!!! This is the home page" 






from blueprints.todo import todo
app.register_blueprint(todo, url_prefix='/api/')


if __name__ == "__main__": 
    app.run()

