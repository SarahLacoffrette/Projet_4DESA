from Database.connectDB import DB
from flask import jsonify, request, Blueprint, render_template, send_file
from Azure.blob import add_blob, get_blob
from datetime import datetime
from azure.storage.blob import generate_blob_sas

media_app = Blueprint('media_app', __name__)


def triMedia(result, size):
    id = []
    title = []
    path = []

    for x in range(0, size):
        id.append(result[x][0])
        title.append(result[x][1])
        path.append(result[x][2])

    return id, title, path
@media_app.route('/getMedia/<filename>', methods=['GET'])
def getMedia_display(filename):

    blob_url = get_blob(filename)
    connection = DB
    with connection.cursor() as cursor:
        sql = "SELECT * FROM media WHERE path = %(filename)s"
        cursor.execute(sql, {
            'filename': filename
        })
        result = cursor.fetchall()
    print("result : ", result)
    return render_template('media_display.html', blob_url=blob_url, title=result[0][1])


@media_app.route('/createMedia', methods=['GET'])
def createMedia_display():
    return render_template('add_media.html')


@media_app.route('/createMedia', methods=['POST'])
def createMedia():
    f = request.files['file']
    title = request.form['title']
    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f)
    file = add_blob(f)

    connection = DB
    with connection.cursor() as cursor:
        sql = "INSERT INTO media (title, date, path) VALUES (%(title)s, %(date)s, %(path)s)"
        cursor.execute(sql, {
            'title': title,
            'date': data,
            'path': file
        })
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        print("result : ", "done")
        return render_template('media.html')



@media_app.route('/modifyMedia/<id>', methods=['PUT'])
def modifyMedia(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = "UPDATE media SET title = %(title)s, date = %(date)s, path = %(path)s WHERE id = " + id
        cursor.execute(sql, request.form)
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)


@media_app.route('/deleteMedia/<id>', methods=['DELETE'])
def deleteMedia(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"DELETE FROM media WHERE id = {id}"
        cursor.execute(sql, request.form)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        new_form = dict(request.form)
        new_form["id"] = cursor.lastrowid
        return jsonify(new_form)


@media_app.route('/media', methods=['GET'])
def viewAllMedias():
    connection = DB
    with connection.cursor() as cursor:
        sql = "SELECT * FROM media"
        cursor.execute(sql)
        result = cursor.fetchall()
        result = list(result)
        size = len(result)
        id, title, path = triMedia(result, size)
        media=[]
        for x in range(0, size):
            media.append(get_blob(path[x]))

        return render_template('media.html', id=id, title=title, path=media, size=size)


@media_app.route('/viewMedia/<id>', methods=['GET'])
def viewMedia(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM media WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)


@media_app.route('/addDownload/<id>', methods=['GET'])
def addDownload(id):
    connection = DB
    with connection.cursor() as cursor:
        sql = f"UPDATE media SET download = download + 1 WHERE id = {id}"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return jsonify(request.form)
