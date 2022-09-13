from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.m1zs4k9.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import pyautogui

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    passwd_receive = str(request.form['passwd_give'])
    commentNum = int(request.form['commentNum_give'])

    print(name_receive)
    print(comment_receive)
    print(passwd_receive)
    print(commentNum)

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'passwd': passwd_receive,
        'commentNum': commentNum
    }

    imsiCommentNum = db.homework.find_one({'commentNum': commentNum})
    print(imsiCommentNum)
    if imsiCommentNum is None:
        db.homework.insert_one(doc)
    else:
        commentNumList = list(db.homework.find({},{'_id':False}))
        print(commentNumList)
        commentNumListLen = len(commentNumList)
        print(commentNumListLen)

        commentNum += commentNumListLen
        doc = {
            'name': name_receive,
            'comment': comment_receive,
            'passwd': passwd_receive,
            'commentNum': commentNum
        }
        db.homework.insert_one(doc)

    return jsonify({'msg':'응원 완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    comment_list = list(db.homework.find({}, {'_id': False}))
    return jsonify({'comments':comment_list})

@app.route("/homework/delete", methods=["POST"])
def homeworkDelete_post():
    commentNum_receive = int(request.form['commentNum_give'])
    passwd_receive = str(request.form['passwd_give'])

    imsiComment = db.homework.find_one({'commentNum': commentNum_receive})
    imsiPasswd = imsiComment['passwd']

    if passwd_receive == imsiPasswd:
        db.homework.delete_one({'commentNum': commentNum_receive})
        return jsonify({'msg': '삭제 완료!'})
    else:
        return jsonify({'msg':'비밀번호를 다시 입력해주세요'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)