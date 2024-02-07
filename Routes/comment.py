from Database.connectDB import DB
from flask import jsonify, request, Blueprint, redirect

comment_app = Blueprint('comment_app', __name__)


def triComments(result, size):
    id = []
    text = []
    id_media = []

    for x in range(0, size):
        id.append(result[x][0])
        text.append(result[x][1])
        id_media.append(result[x][2])

    return id, text, id_media

def getAllComments():
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT comment.id, comment.text, comment.id_media FROM comment"
        cursor.execute(sql)
        result = cursor.fetchall()
        result = list(result)
        size = len(result)
        id, text, id_media = triComments(result, size)
        return id, text, id_media, size


@comment_app.route('/createComment', methods=['POST'])
def createComment():
    connection = DB
    text = request.form['text']
    id_media = request.form['id_media']
    with connection.cursor() as cursor:
        sql = "INSERT INTO comment (text, id_media) VALUES (%(text)s, %(id_media)s)"
        cursor.execute(sql, {
            'text': text,
            'id_media': id_media
        })
        result = cursor.fetchall()
        connection.commit()
        return redirect('/media')


@comment_app.route('/modifyComment/<id>', methods=['PUT'])
def modifyComment(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = "UPDATE comment SET text = %(text)s WHERE id = " + id
        cursor.execute(sql, request.form)
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)

@comment_app.route('/deleteComment/<id>', methods=['DELETE'])
def deleteComment(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"DELETE FROM comment WHERE id = {id}"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)