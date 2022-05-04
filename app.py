from flask import Flask, request, render_template, jsonify, make_response
from model.dbmodel import con_pool
from model.s3model import s3
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    text = request.values.get("text")
    filename = file.filename
    s3.Bucket("myawscloudfiles").put_object(
        Key=file.filename, Body=file)
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        sql = "Insert Into data(text,imgurl) Values( %s, %s)"
        val = (text, f"https://d33yfiwdj1z4d4.cloudfront.net/{filename}")
        cursor.execute(sql, val)
        cursor.execute("select * from data ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
    except:
        db.rollback()
    finally:
        db.commit()
        cursor.close()
        db.close()
    return {"text": result["text"], "imgurl": result["imgurl"]}


@app.route("/getdata", methods=["get"])
def getdata():
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("select * from data ")
        result = cursor.fetchall()
        return {"data": result}
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0",port="5000")
