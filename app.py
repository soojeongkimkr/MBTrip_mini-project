from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.xvovm.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mbtrip", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    return jsonify({'msg': '추가 완료'})

@app.route("/mbtrip", methods=["GET"])
def comment_get():
    return jsonify({'comments': comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)