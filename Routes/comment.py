from app import app
from connectDB import DB
from flask import jsonify, request

@app.route('/createComment', methods=['POST'])
def createComment():
    connection = DB()
    with connection.cursor() as cursor:
        sql = "INSERT INTO comment (text, id_user, id_media) VALUES (%(text)s, %(id_user)s, %(id_media)s"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return jsonify(request.form)


@app.route('/modifyComment/<id>', methods=['PUT'])
def modifyComment(id):
    connection = DB()
    with connection.cursor() as cursor:
        sql = "UPDATE comment SET text = %(text)s WHERE id = " + id
        cursor.execute(sql, request.form)
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)

@app.route('/deleteComment/<id>', methods=['DELETE'])
def deleteComment(id):
    connection = DB()
    with connection.cursor() as cursor:
        sql = f"DELETE FROM comment WHERE id = {id}"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)