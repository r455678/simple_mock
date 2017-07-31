#coding=utf-8
from  flask import Flask,request,jsonify
import pymysql
from datetime import datetime

app=Flask(__name__)
config ={
        'host':'192.168.20.155',
        'port':3306,
        'user':'test',
        'passwd':'test123',
        'db':'cts',
        'charset':'utf8',
        }

@app.route('/addinfo',methods=['POST'])
def  query_user():
    title=request.form['title']
    method=request.form['method']
    reqparams=request.form['reqparams']
    resparams=request.form['resparams']
    des=request.form['des']
    domain=request.form['domain']
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('insert into mock_config (title,reqparams,methods,domain,description,resparams,status) '
                    'values (%s,%s,%s,%s,%s,%s,%s) ',(title,reqparams,method,domain,des,resparams,0))
        conn.commit()
        conn.close()
    except :
        return jsonify({'msg': "fail", "remark": "save data fail"})
    return jsonify({'msg': "ok","remark":""})

@app.route('/delinfo',methods=['POST'])
def  delinfo():
    id=request.form['id']
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('delete from mock_config where id=%s',(id))
        conn.commit()
        conn.close()
    except :
        return jsonify({'msg': "fail", "remark": "delete fail"})
    return jsonify({'msg': "ok","remark":""})

@app.route('/editinfo',methods=['POST'])
def  editinfo():
    title = request.form['title']
    method = request.form['method']
    reqparams = request.form['reqparams']
    resparams = request.form['resparams']
    des = request.form['reqparams']
    domain = request.form['domain']
    id=request.form['id']
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('update mock_config set title=%s,reqparams=%s,methods=%s,domain=%s,description=%s,resparams=%s,update_time=%s where id=%s',(title, reqparams, method, domain, des, resparams,datetime.now().strftime('%y-%m-%d %H:%M:%S'),id))
        conn.commit()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "save data fail"})
    return jsonify({'msg': "ok", "remark": ""})

@app.route('/selectinfo',methods=['GET'])
def  selectinfo():
    id=request.args.get("id")
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('select title,reqparams,methods,domain,description,resparams from mock_config where id=%s',(id))
        re= cur.fetchone()
        conn.close()
    except:
        return jsonify({'msg': "ok", "remark": "select data fail"})
    return jsonify({'msg': "fail", "remark": "", "title": re[0], "method": re[2], "reqparams": re[1], "domain": re[3],"resparams": re[5], "des": re[4]})

@app.route('/manage',methods=['POST'])
def  manage():
    id = request.form['id']
    status = request.form['status']
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('update mock_config set status=%s where id=%s',(status,id))
        conn.commit()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": ""})

@app.route('/search',methods=['GET'])
def  search():
    title=request.args.get("title")
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('select title,reqparams,methods,domain,description,resparams from mock_config where title=%s',(title))
        re= cur.fetchall()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": re})

@app.route('/searchall',methods=['GET'])
def  searchall():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('select title,reqparams,methods,domain,description,resparams from mock_config')
        re= cur.fetchall()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": re})


if __name__=="__main__":
    app.run(debug=True,threaded=True)

