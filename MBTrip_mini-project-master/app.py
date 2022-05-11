from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb://15.164.98.100', 27017, username="test", password="test")
db = client.dbsparta_plus_week4


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/ENTP')
def detail():
    return  render_template("entp.html")

@app.route('/ENFJ')
def enfj():
    return  render_template("enfj.html")

@app.route('/ENFP')
def enfp():
    return  render_template("enfp.html")

@app.route('/ENTJ')
def entj():
    return  render_template("entj.html")

@app.route('/ESFJ')
def esfj():
    return  render_template("esfj.html")

@app.route('/ESFP')
def esfp():
    return  render_template("esfp.html")

@app.route('/ESTJ')
def estj():
    return  render_template("estj.html")

@app.route('/estp')
def estp():
    return  render_template("estp.html")

@app.route('/INFJ')
def infj():
    return  render_template("infj.html")

@app.route('/INFP')
def infp():
    return  render_template("infp.html")

@app.route('/INTJ')
def intj():
    return  render_template("intj.html")

@app.route('/INTP')
def intp():
    return  render_template("intp.html")

@app.route('/ISFJ')
def isfj():
    return  render_template("isfj.html")

@app.route('/ISFP')
def isfp():
    return  render_template("isfp.html")

@app.route('/ISTJ')
def istj():
    return  render_template("istj.html")

@app.route('/ISTP')
def istp():
    return  render_template("istp.html")





#사용자가 작성한 리뷰를 db에 저장
@app.route('/write', methods=['POST'])
def write_review():
    # 현재 이용자의 컴퓨터에 저장된 cookie에서 mytoken을 가져온다.
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})

        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        print(type(date_receive))

        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.reviews.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/review', methods=['GET'])
def show_review():
    # 현재 이용자의 컴퓨터에 저장된 cookie에서 mytoken을 가져온다.
    token_receive = request.cookies.get('mytoken')

    try:
        #암호화되어있는 token의 값을 우리가 사용할 수 있도록 디코딩(암호화 풀기) 해준다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]

        if username == "":
            reviews = list(db.reviews.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.reviews.find({"username": username}).sort("date", -1).limit(10))

        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))


@app.route('/delete', methods=['POST'])
def delete_review():
    # 리뷰 삭제
    id_receive = request.form["id_give"]
    db.reviews.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})


@app.route('/like', methods=['POST'])
def like_review():
    review_receive = request.form['review_give']
    target_review = db.reviews.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1

    db.reviews.update_one({'write': review_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

