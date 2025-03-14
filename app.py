from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def read_memos():

    result = list(db.memos.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'memos': result})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_memos():
    title_receive = request.form['title_give']  # 클라이언트로부터 title을 받는 부분
    content_receive = request.form['content_give']  # 클라이언트로부터 content를 받는 부분

    if not title_receive or not content_receive:
        return jsonify({'result': 'fail', 'msg': '제목과 내용을 입력하세요'}), 400


    memo = {'title': title_receive, 'content': content_receive, 'like': 0}

    db.memos.insert_one(memo)

    return jsonify({'result': 'success'})


# 삭제 기능능
@app.route('/memo/delete', methods=['POST'])
def delete_memo():
        title_receive = request.form.get('title_give')

        db.memos.delete_one({'title': title_receive})
        return jsonify({'result': 'success'})
 

# 좋아요 기능
@app.route('/memo/like', methods=['POST'])
def like_memo():
        title_receive = request.form.get('title_give')

        db.memos.update_one({'title': title_receive}, {'$inc': {'like': 1}})
        return jsonify({'result': 'success'})

# 수정 기능
@app.route('/memo/update', methods=['POST'])
def update_memo():
    title = request.form['title']
    new_title = request.form['new_title']
    new_content = request.form['new_content']
    
    db.memos.update_one({'title': title}, {'$set': {'title': new_title, 'content': new_content}})
    return jsonify({'result': 'success'})

def select() :
     return 0

def select_one() :
     return 0

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)