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

@app.route('/entp')
def entp():
    return render_template("entp.html")

@app.route('/enfj')
def enfj():
    return  render_template("enfj.html")

@app.route('/enfp')
def enfp():
    return  render_template("enfp.html")

@app.route('/entj')
def entj():
    return  render_template("entj.html")

@app.route('/esfj')
def esfj():
    return  render_template("esfj.html")

@app.route('/esfp')
def esfp():
    return  render_template("esfp.html")

@app.route('/estj')
def estj():
    return  render_template("estj.html")

@app.route('/estp')
def estp():
    return  render_template("estp.html")

@app.route('/infj')
def infj():
    return  render_template("infj.html")

@app.route('/infp')
def infp():
    return  render_template("infp.html")

@app.route('/intj')
def intj():
    return  render_template("intj.html")

@app.route('/intp')
def intp():
    return  render_template("intp.html")

@app.route('/isfj')
def isfj():
    return  render_template("isfj.html")

@app.route('/isfp')
def isfp():
    return  render_template("isfp.html")

@app.route('/istj')
def istj():
    return  render_template("istj.html")

@app.route('/istp')
def istp():
    return  render_template("istp.html")

@app.route('/write/enfj', methods=['POST'])
def enfj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.enfj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/enfj', methods=['GET'])
def enfj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.enfj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.enfj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/enfj', methods=['POST'])
def enfj_delete_review():
    id_receive = request.form["id_give"]
    db.enfj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/enfj', methods=['POST'])
def enfj_like_review():
    review_receive = request.form['review_give']
    target_review = db.enfj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.enfj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/enfp', methods=['POST'])
def enfp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.enfp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/enfp', methods=['GET'])
def enfp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.enfp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.enfp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/enfp', methods=['POST'])
def enfp_delete_review():
    id_receive = request.form["id_give"]
    db.enfp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/enfp', methods=['POST'])
def enfp_like_review():
    review_receive = request.form['review_give']
    target_review = db.enfp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.enfp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/entj', methods=['POST'])
def entj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.entj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/entj', methods=['GET'])
def entj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.entj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.entj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/entj', methods=['POST'])
def entj_delete_review():
    id_receive = request.form["id_give"]
    db.entj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/entj', methods=['POST'])
def entj_like_review():
    review_receive = request.form['review_give']
    target_review = db.entj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.entj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/entp', methods=['POST'])
def entp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.entp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/entp', methods=['GET'])
def entp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.entp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.entp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/entp', methods=['POST'])
def entp_delete_review():
    id_receive = request.form["id_give"]
    db.entp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/entp', methods=['POST'])
def entp_like_review():
    review_receive = request.form['review_give']
    target_review = db.entp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.entp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/esfj', methods=['POST'])
def esfj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.esfj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/esfj', methods=['GET'])
def esfj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.esfj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.esfj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/esfj', methods=['POST'])
def esfj_delete_review():
    id_receive = request.form["id_give"]
    db.esfj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/esfj', methods=['POST'])
def esfj_like_review():
    review_receive = request.form['review_give']
    target_review = db.esfj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.esfj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/esfp', methods=['POST'])
def esfp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.esfp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/esfp', methods=['GET'])
def esfp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.esfp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.esfp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/esfp', methods=['POST'])
def esfp_delete_review():
    id_receive = request.form["id_give"]
    db.esfp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/esfp', methods=['POST'])
def esfp_like_review():
    review_receive = request.form['review_give']
    target_review = db.esfp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.esfp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/estj', methods=['POST'])
def estj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.estj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/estj', methods=['GET'])
def estj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.estj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.estj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/estj', methods=['POST'])
def estj_delete_review():
    id_receive = request.form["id_give"]
    db.estj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/estj', methods=['POST'])
def estj_like_review():
    review_receive = request.form['review_give']
    target_review = db.estj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.estj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/estp', methods=['POST'])
def estp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.estp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/estp', methods=['GET'])
def estp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.estp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.estp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/estp', methods=['POST'])
def estp_delete_review():
    id_receive = request.form["id_give"]
    db.estp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/estp', methods=['POST'])
def estp_like_review():
    review_receive = request.form['review_give']
    target_review = db.estp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.estp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/infj', methods=['POST'])
def infj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.infj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/infj', methods=['GET'])
def infj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.infj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.infj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/infj', methods=['POST'])
def infj_delete_review():
    id_receive = request.form["id_give"]
    db.infj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/infj', methods=['POST'])
def infj_like_review():
    review_receive = request.form['review_give']
    target_review = db.infj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.infj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/infp', methods=['POST'])
def infp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.infp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/infp', methods=['GET'])
def infp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.infp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.infp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/infp', methods=['POST'])
def infp_delete_review():
    id_receive = request.form["id_give"]
    db.infp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/infp', methods=['POST'])
def infp_like_review():
    review_receive = request.form['review_give']
    target_review = db.infp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.infp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/intj', methods=['POST'])
def intj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.intj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/intj', methods=['GET'])
def intj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.intj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.intj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/intj', methods=['POST'])
def intj_delete_review():
    id_receive = request.form["id_give"]
    db.intj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/intj', methods=['POST'])
def intj_like_review():
    review_receive = request.form['review_give']
    target_review = db.intj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.intj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/intp', methods=['POST'])
def intp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.intp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/intp', methods=['GET'])
def intp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.intp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.intp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/intp', methods=['POST'])
def intp_delete_review():
    id_receive = request.form["id_give"]
    db.intp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/intp', methods=['POST'])
def intp_like_review():
    review_receive = request.form['review_give']
    target_review = db.intp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.intp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/isfj', methods=['POST'])
def isfj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.isfj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/isfj', methods=['GET'])
def isfj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.isfj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.isfj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/isfj', methods=['POST'])
def isfj_delete_review():
    id_receive = request.form["id_give"]
    db.isfj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/isfj', methods=['POST'])
def isfj_like_review():
    review_receive = request.form['review_give']
    target_review = db.isfj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.isfj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/isfp', methods=['POST'])
def isfp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.isfp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/isfp', methods=['GET'])
def isfp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.isfp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.isfp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/isfp', methods=['POST'])
def isfp_delete_review():
    id_receive = request.form["id_give"]
    db.isfp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/isfp', methods=['POST'])
def isfp_like_review():
    review_receive = request.form['review_give']
    target_review = db.isfp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.isfp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/istj', methods=['POST'])
def istj_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.istj.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/istj', methods=['GET'])
def istj_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.istj.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.istj.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/istj', methods=['POST'])
def istj_delete_review():
    id_receive = request.form["id_give"]
    db.istj.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/istj', methods=['POST'])
def istj_like_review():
    review_receive = request.form['review_give']
    target_review = db.istj.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.istj.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

@app.route('/write/istp', methods=['POST'])
def istp_write_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        write_receive = request.form['write_give']
        date_receive = request.form['date_give']
        doc = {
            "username" : user_info["username"],
            "write": write_receive,
            "date": date_receive,
            "like" : 0,
        }
        db.istp.insert_one(doc)
        return jsonify({"result": "success", 'msg': '작성 성공'})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/review/istp', methods=['GET'])
def istp_show_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        if username == "":
            reviews = list(db.istp.find({}).sort("date", -1).limit(10))
        else:
            reviews = list(db.istp.find({"username": username}).sort("date", -1).limit(10))
        for review in reviews:
            review["_id"] = str(review["_id"])
        return jsonify({"result": "success", "reviews": reviews})
    except (jwt.ExpiredSignature, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
@app.route('/delete/istp', methods=['POST'])
def istp_delete_review():
    id_receive = request.form["id_give"]
    db.istp.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({ 'msg': '리뷰 삭제'})
@app.route('/like/istp', methods=['POST'])
def istp_like_review():
    review_receive = request.form['review_give']
    target_review = db.istp.find_one({'write': review_receive})
    current_review = target_review['like']
    new_like = current_review + 1
    db.istp.update_one({'write': review_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

