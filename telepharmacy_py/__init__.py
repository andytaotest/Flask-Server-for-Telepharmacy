import os

from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    run_with_ngrok(app)
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'telepharmacy.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    #@app.route("/login", methods=["GET", "POST"])
    #def do_login():
        #username = request.form.get("username")
        #password = request.form.get("password")
        #if username == "kenneth":
            #if password == "pass123":
                #account = {
                    #"username": username,
                    #"result": True
                    #}
            #else:
                #account = {
                    #"username": username,
                    #"result": False
                    #}
        #else:
            #account = {
                #"username": "no_user",
                #"result": False
                #}
        #return account

    return app