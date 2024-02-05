from app import app
from connectDB import DB
from flask import jsonify, request

@app.route('/createMedia', methods=['POST'])
def createMedia():
    connection = DB()
    with connection.cursor() as cursor:
        sql = "INSERT INTO media (name, date, path) VALUES (%(name)s, %(date)s, %(path)s"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return jsonify(request.form)

@app.route('/modifyMedia/<id>', methods=['PUT'])
def modifyMedia(id):
    connection = DB()
    with connection.cursor() as cursor:
        sql = "UPDATE media SET name = %(name)s, date = %(date)s, path = %(path)s WHERE id = " + id
        cursor.execute(sql, request.form)
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)

@app.route('/deleteMedia/<id>', methods=['DELETE'])
def deleteMedia(id):
    connection = DB()
    with connection.cursor() as cursor:
        sql = f"DELETE FROM media WHERE id = {id}"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)

@app.route('/viewAllMedias', methods=['GET'])
def viewAllMedias():
    connection = DB()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM media"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)

@app.route('/viewMedia/<id>', methods=['GET'])
def viewMedia(id):
    connection = DB()
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM media WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)

@app.route('/addDownload/<id>', methods=['GET'])
def addDownload(id):
    connection = DB()
    with connection.cursor() as cursor:
        sql = f"UPDATE media SET download = download + 1 WHERE id = {id}"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return jsonify(request.form)