import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        result = None

        if not username:
            result = 'Username is required.'
        elif not password:
            result = 'Password is required.'

        if result is None:
            try:
                query = db.execute(
                    "SELECT * FROM account WHERE username = ?",
                    (username,),
                ).fetchone()
                if query:
                    print(check_password_hash(generate_password_hash(password), password))
                    print(type(query[2]))
                    print(type(password))
                    if check_password_hash(query[2], password):
                        print("check password is true, password hash is " + query[2] + " and password is " + password)
                        result = {
                            "result": "success",
                            "username": query[1],
                            "type":query[3],
                            "pharmacistId":query[4]
                        }
                        print(result)
                    else:
                        print("check password is false, password hash is " + query[2] + " and password is " + password)
                        result = {
                            "result" : "Incorrect username/password"
                        }
                    print("\n\n\nquery got something")
                    print(query)
                    
                    #else:
                        #result = "Incorrect password"
                else:
                    print("\n\n\nquery got nothing")
                    print(query)
                    result = {
                        "result": "No such username found"
                    }
            except db.IntegrityError:
                result = {
                    "result": "Error fetching from database"
                }
    return result

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        userType = request.form["type"]
        pharmacistId = request.form["pharmacistid"]
        pharmacistFound = None
        pharmacistAccount = None
        db = get_db()
        result = None

        if not username:
            result = 'Username is required.'
        elif not password:
            result = 'Password is required.'
        
        if userType == "pharmacist":
            if pharmacistId:
                try:
                    pharmacistFound = db.execute(
                        "SELECT * FROM pharmacist WHERE pharmacist_id = ?",
                        (pharmacistId,),
                    ).fetchone()
                    if not pharmacistFound:
                        result = "No such pharmacist ID"
                    else:
                        pharmacistAccount = db.execute(
                            "SELECT * FROM account WHERE pharmacist_id = ?",
                            (pharmacistId,),
                        ).fetchone()
                        if pharmacistAccount:
                            result = "Account already exists for pharmacist"
                except db.IntegrityError:
                    result = "Error fetching from database"
            else:
                result = "Please enter your Pharmacist ID"
        
        if result is None:
            try:
                result = db.execute(
                    "INSERT INTO account (username, password, type, pharmacist_id) VALUES (?, ?, ?, ?)",
                    (username, generate_password_hash(password), userType, pharmacistId),
                )
                result = "true"
                db.commit()
            except db.IntegrityError:
                result = "Username already exists"

    return result

@bp.route("/room", methods=["GET", "POST"])
def room():
    if request.method == 'POST':
        pharmacistId = request.form["pharmacistId"]
        db = get_db()
        result = None

        if not pharmacistId:
            result = 'Error, not logged in as Pharmacist. You should not be seeing this screen.'

        if result is None:
            try:
                query = db.execute(
                    "SELECT * FROM pharmacist WHERE pharmacist_id = ?",
                    (pharmacistId,),
                ).fetchone()
                if query:
                    print("\n\n\nROOM query got something")
                    print(query)                    
                    result = {
                        "result": "success",
                        "pharmacistId": query[0],
                        "name": query[1],
                        "email": query[2],
                        "roomId": query[3]
                        }
                else:
                    print("\n\n\nROOM query got nothing")
                    print(query)
                    result = {
                        "result": "Error, no such pharmacist found."
                    }
            except db.IntegrityError:
                result = {
                    "result": "Error fetching from database"
                }
    return result

#def do_login():
    #username = request.form.get("username")
    #password = request.form.get("password")
    #account = {
        #"username": username,
        #"password": password
        #}
    #return jsonify(result=True)