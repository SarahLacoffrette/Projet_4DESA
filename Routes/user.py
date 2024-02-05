from connectDB import DB
from flask import jsonify, request
from flask import Blueprint


user_app = Blueprint('user_app', __name__)

@user_app.route('/createUser', methods=['POST'])
def createUser():
    connection = DB
    with connection.cursor() as cursor:
        sql = "INSERT INTO user (name, firsname, username, password, state, role) VALUES (%(name)s, %(firstname)s, %(username)s, %(password)s, %(state)s, %(role)s"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return jsonify(request.form)

@user_app.route('/modifyUser/<id>', methods=['PUT'])
def modifyUser(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = "UPDATE user SET name = %(name)s, firstname = %(firstname)s, username = %(username)s, password = %(password)s, state = %(state)s, role = %(role)s WHERE id = " + id
        cursor.execute(sql, request.form)
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)

@user_app.route('/deleteUser/<id>', methods=['DELETE'])
def deleteUser(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"DELETE FROM user WHERE id = {id}"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)

@user_app.route('/viewAllUsers', methods=['GET'])
def viewAllUsers():
    connection = DB
    print("hey")
    with connection.cursor() as cursor:
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)

@user_app.route('/viewUser/<id>', methods=['GET'])
def viewUser(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM user WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)

