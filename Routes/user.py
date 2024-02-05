import os
from Database.connectDB import DB
from flask import jsonify, request, render_template, Blueprint, redirect, url_for, session

user_app = Blueprint('user_app', __name__)

def is_authenticated(username, password):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return False
        else:
            return True

def is_connected():
    print("enter")
    if 'username' in session:
        print("1")
        return True
    else:
        print("2")
        return False

def get_role(username):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT role FROM user WHERE username = '{username}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]

def triProfil(result, size):
    id = []
    name = []
    firstname = []
    username = []
    role = []
    stateUser = []

    for x in range(0, size):
        id.append(result[x][0])
        name.append(result[x][1])
        firstname.append(result[x][2])
        username.append(result[x][3])
        role.append(result[x][4])
        stateUser.append(result[x][5])

    return id, name, firstname, username, role, stateUser

@user_app.route('/createUser', methods=['Get'])
def createUser_display():
    return render_template('register.html')
@user_app.route('/createUser', methods=['POST'])
def createUser():
    connection = DB
    with connection.cursor() as cursor:
        name = request.form['name']
        firstname = request.form['firstname']
        username = request.form['username']
        password = request.form['password']
        stateUser = 1
        role = 1

        print(name, firstname, username, password)

        sql = "INSERT INTO user (name, firstname, username, password, stateUser, role) VALUES (%(name)s, %(firstname)s, %(username)s, %(password)s, %(stateUser)s, %(role)s)"
        cursor.execute(sql, {'name': name, 'firstname': firstname, 'username': username, 'password': password, 'stateUser': stateUser, 'role': role})
        connection.commit()
        return jsonify(request.form)

@user_app.route('/dashboard', methods=['GET'])
def modifyUser_display():
    if is_connected():
        if 'username' in session:
            print("session", session)
            username = session['username']
            connection = DB
            with connection.cursor() as cursor:
                sql = "SELECT user.id, user.name, user.firstname, user.username, user.role, user.stateUser FROM user WHERE username = '" + username + "'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                result = list(result)
                size = len(result)
                print("size", size)
                print("result", result)
                id, name, firstname, username, role, stateUser = triProfil(result, size)
                return render_template('profile.html', size=size , id=id[0], name=name[0], firstname=firstname[0], username=username[0])
    else :
        return redirect(url_for('user_app.login'))

@user_app.route('/modifyUser', methods=['POST'])
def updateUser():
    connection = DB
    id = request.form['id']
    name = request.form['name']
    firstname = request.form['firstname']
    password = request.form['password']

    with connection.cursor() as cursor:
        sql = "UPDATE user SET name = %(name)s, firstname = %(firstname)s, password = %(password)s WHERE id = " + id
        cursor.execute(sql, {
            'id': id,
            'name': name,
            'firstname': firstname,
            'password': password
        })
        connection.commit()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return redirect(url_for('user_app.modifyUser_display'))

@user_app.route('/deleteUser', methods=['POST'])
def deleteUser():
    id = request.form['user_id']
    print("id", id)
    connection = DB
    with connection.cursor() as cursor:
        sql = f"DELETE FROM user WHERE id = {id}"
        cursor.execute(sql, {
            'id': id
        })
        result = cursor.fetchall()
        connection.commit()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)


@user_app.route('/viewUser/<id>', methods=['GET'])
def viewUser(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM user WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(result)


@user_app.route('/viewUserByUsername/<username>/<password>', methods=['GET'])
def viewUserbyusername(username, password):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result) == 0):
            return jsonify("no user")
        else:
            return jsonify(result)
@user_app.route('/listeUsers', methods=['GET'])
def listeUsers():
    if(is_connected()):
        if(session['role'] != 2):
            return redirect(url_for('user_app.dashboard'))
        else :
            connection = DB
            with connection.cursor() as cursor:
                sql = "SELECT user.id, user.name, user.firstname, user.username, user.role, user.stateUser FROM user"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                result = list(result)
                size = len(result)
                print("size", size)
                print("result", result)
                id, name, firstname, username, role, stateUser = triProfil(result, size)
                return render_template('listeUsers.html', size=size , id=id, name=name, firstname=firstname, username=username, role=role, stateUser=stateUser)
    else:
        return redirect(url_for('user_app.login'))

@user_app.route('/login', methods=['GET'])
def login_display():
    return render_template('login.html')

@user_app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if is_authenticated(username, password):
        session['username'] = username
        session['role'] = get_role(username)
        print(session)
        return redirect(url_for('user_app.dashboard'))
    else:
        return 'Identifiants invalides <a href="/">Accueil</a>'

#@user_app.route('/dashboard')
def dashboard():
    if 'username' in session:
        print("session", session)
        username = session['username']
        role = session['role']
        return render_template('profile.html', username=username, role=role)
    else:
        return redirect(url_for('user_app.login'))

@user_app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Vous avez été déconnecté. <a href="/login">Se connecter à nouveau</a>'

