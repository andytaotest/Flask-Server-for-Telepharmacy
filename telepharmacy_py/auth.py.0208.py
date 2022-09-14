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
                    "SELECT * FROM account WHERE username = ? and status = ?",
                    (username, 'active',),
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
                        "result": "Incorrect username/password"
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
        userType = request.form["type"]
        password = request.form["password"]
        pharmacistId = request.form["pharmacistid"]
        date_created = request.form["date_created"]
        pharmacistFound = None
        pharmacistAccount = None
        userFound = None
        verified = None
        db = get_db()
        result = None

        if not username:
            result = 'Username is required.'
        elif not password:
            result = 'Password is required.'
        
        if userType == "pharmacist":
            if pharmacistId:
                userVerification = request.form["verification"]
                try:
                    pharmacistFound = db.execute(
                        "SELECT * FROM pharmacist WHERE pharmacist_id = ?",
                        (pharmacistId,),
                    ).fetchone()
                    if not pharmacistFound:
                        result = "No such pharmacist ID"
                        print("no pharmacist found")
                    else:
                        pharmacistAccount = db.execute(
                            "SELECT * FROM account WHERE pharmacist_id = ?",
                            (pharmacistId,),
                        ).fetchone()
                        if pharmacistAccount:
                            result = "Account already exists for pharmacist"
                        else:
                            try:
                                verified = db.execute(
                                "SELECT * FROM pharmacist WHERE pharmacist_id = ? AND verification = ?", 
                                (pharmacistId, userVerification,),
                                ).fetchone()
                                if not verified:
                                    result = "Verification failed: Invalid code"
                            except db.IntegrityError:
                                    result = "db Integrity Error from verification check, Error fetching from database"
                except db.IntegrityError:
                    result = "Error fetching from database"
            else:
                result = "Please enter your Pharmacist ID"
           

        if result is None:
            try:
                userFound = db.execute(
                "SELECT * FROM account WHERE username = ?",
                (username,),
                ).fetchone()
                if userFound:
                    result = "Invalid username, please use another"
                else:
                    try:
                        result = db.execute(
                        "INSERT INTO account (username, password, type, pharmacist_id, status, date_created) VALUES (?, ?, ?, ?, ?, ?)",
                        # insert date created at the end
                        (username, generate_password_hash(password), userType, pharmacistId, "active", date_created),
                        )
                        db.commit()
                        result = "true"
                    except db.IntegrityError:
                        result = "Error registering user into database"
            except db.IntegrityError:
                result = "Error fetching users from database"
            

    return result

# @bp.route("/verify", methods=["GET", "POST"])
# def verify():
#     if request.method == 'POST':
#         username = request.form["username"]
#         password = request.form["password"]
#         userType = request.form["type"]
#         pharmacistId = request.form["pharmacistid"]
#         userVerification = request.form["verification"]
#         db = get_db()
#         result = None
#         verified = None
#         print(username, password, userType, pharmacistId, userVerification)

#         if userType == "pharmacist":
#             try:
#                 verified = db.execute(
#                 "SELECT * FROM pharmacist WHERE pharmacist_id = ? AND verification = ?", 
#                 (pharmacistId, userVerification,),
#                 ).fetchone()
#                 if not verified:
#                     result = "Verification failed: Invalid code"
#                 else:
#                     verified = True
#             except db.IntegrityError:
#                     result = "db Integrity Error from verification check, Error fetching from database"
#         else:
#             if userVerification == "123456":
#                 verified = True
#             else:
#                 result = "Verification failed: Invalid code"
            
#         if result is None and verified:
#             try:
#                 result = db.execute(
#                     "INSERT INTO account (username, password, type, status, pharmacist_id) VALUES (?, ?, ?, ?, ?)",
#                     (username, generate_password_hash(password), userType, "active", pharmacistId),
#                 )
#                 db.commit()
#                 result = "true"
#             except db.IntegrityError:
#                 result = "db Integrity Error from inserting, User already exists"

#     return result




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


@bp.route("/order", methods=["GET", "POST"])
def order():
    if request.method == 'POST':
        username = request.form["username"]
        db = get_db()
        result = None
        orders = {}
        ind_num = 0

        if result is None:
            try:
                query = db.execute(
                    "SELECT * FROM orders WHERE username = ?",
                    (username,),
                ).fetchall()
                if query:
                    for rows in query:
                        item = {
                            "orderid": rows[2],
                            "symptoms": rows[3],
                            "expirydate":rows[4],
                            "timestamp":rows[5],
                        }
                        index = "order"+str(ind_num)
                        orders[index]=item
                        ind_num += 1
                   
                    result = orders
                    print("\n\n\nquery got something")
                    print(query)
                    
                else:
                    print("\n\n\nquery got nothing")
                    print(query)
                    result = {
                        "result": "None"
                    }
            except db.IntegrityError:
                result = {
                    "result": "Error fetching from database"
                }

    return result

@bp.route("/insert_order", methods=["GET", "POST"])
def insert_order():
    if request.method == 'POST':
        order_id = request.form["order_id"]
        username = request.form["username"]
        symptoms = request.form["symptoms"]
        expirydate = request.form["expirydate"]
        timestamp = request.form["timestamp"]
        db = get_db()
        result = None
        
        if result is None:
            try:
                query = db.execute(
                    "SELECT * FROM account WHERE username = ? AND status = ?",
                    (username, "active"),
                ).fetchone()
                if query:
                    result = db.execute(
                        "INSERT INTO orders (username, order_id, symptoms, expiry_date, issue_date) VALUES (?, ?, ?, ?, ?)",
                        (username, order_id, symptoms, expirydate, timestamp),
                    )
                    result = {
                        "result": "found"
                    }
                    db.commit()
                    print("\n\n\nquery got something")
                    print(query)
                else:
                    print("\n\n\nquery got nothing")
                    print(query)
                    result = {
                        "result": "failed"
                    }
            except db.IntegrityError:
                    result = {
                        "result": "Error fetching from database"
                    }

    return result

@bp.route("/password", methods=["GET", "POST"])
def password():
    if request.method == 'POST':
        username = request.form["username"]
        oldpassword = request.form["oldpassword"]
        newpassword = request.form["newpassword"]
        db = get_db()
        result = None

        if not username:
            result = {
                "result": "Username is required"
            }
        elif not oldpassword:
            result = {
                "result": "Current Password is required"
            }
        elif not newpassword:
            result = {
                "result": "New Password is required"
            }
        if oldpassword == newpassword:
            result = {
                "result": "New password cannot be the same as Current password"
            }

        if result is None:
            try:
                query = db.execute(
                    "SELECT * FROM account WHERE username = ?",
                    (username,),
                ).fetchone()
                if query:
                    print(check_password_hash(generate_password_hash(oldpassword), oldpassword))
                    print(type(query[2]))
                    print(type(oldpassword))
                    if check_password_hash(query[2], oldpassword):
                        print("check password is true, password hash is " + query[2] + " and password is " + oldpassword)
                        result = {
                            "result": "success",
                            "username": query[1],
                            "type":query[3],
                            "pharmacistId":query[4]
                        }
                        print(result)
                        query = db.execute(
                            "UPDATE account SET password = ? WHERE username = ?",
                            (generate_password_hash(newpassword), username)
                        )
                        db.commit()
                        result = {
                            "result": "Change Success"
                        }
                    else:
                        print("check password is false, password hash is " + query[2] + " and password is " + oldpassword)
                        result = {
                            "result" : "Incorrect password"
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

@bp.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == 'POST':
        username = request.form["username"]
        update_date = request.form["update"]
        user_type = request.form["type"]
        db = get_db()
        result = None

        if not username:
            result = "Error, you should not be on this page"

        if result is None:
            if user_type == "pharmacist":
                try:
                    result = db.execute(
                    "UPDATE account SET status = ?, pharmacist_id = ?, date_updated = ? WHERE username = ? AND status = ?",
                    ('deleted', 'DEL-PT', update_date, username, 'active')
                    )
                    db.commit()
                    result = 'true'
                except db.IntegrityError:
                    result = 'Error deleting account'
            else:
                try:
                    result = db.execute(
                    "UPDATE account SET status = ?, date_updated = ? WHERE username = ? AND status = ?",
                    ('deleted', update_date, username, 'active')
                    )
                    db.commit()
                    result = 'true'
                except db.IntegrityError:
                    result = 'Error deleting account'
            

    return result

#def do_login():
    #username = request.form.get("username")
    #password = request.form.get("password")
    #account = {
        #"username": username,
        #"password": password
        #}
    #return jsonify(result=True)