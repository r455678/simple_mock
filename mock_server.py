# -*- coding: utf-8 -*-
from flask import jsonify, Flask,make_response,request
import pymysql
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

cf = ConfigParser.ConfigParser()
path = 'db.config'
cf.read(path)
cf.read(path)
secs = cf.sections()
_host= cf.get("database","dbhost")
_port= cf.get("database","dbport")
_dbname=cf.get("database","dbname")
_dbuser=cf.get("database","dbuser")
_dbpassword=cf.get("database","dbpassword")
_path=cf.get("path","filepath")

config ={
        'host':_host,
        'port':int(_port),
        'user':_dbuser,
        'passwd':_dbpassword,
        'db':_dbname,
        'charset':'utf8',
        }

def checkpath(domain,varsvalue,method):
    varsvalue.sort()
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    size = cur.execute('select * from mock_config where domain=%s', (domain))  # 校验domain是否存在
    size1 = cur.execute('select * from mock_config where methods=%s', (method))  # 校验method是否存在
    conn.close()
    if size == 0:
        return jsonify({"msg": "请求方法不存在"})
    elif size1 == 0:
        return jsonify({"msg": "请求模式不存在"})

    if len(varsvalue) == 0:
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute('select resparams from mock_config where status=0 and domain=%s and methods=%s', (domain, method))
        resparams = cur.fetchone()
        conn.close()
        if resparams[0] == '':
            return jsonify({"msg": "对应请求没有配置预期返回值"})
        else:
            return resparams[0].encode("utf-8")
    else:
        varsvalue1=getvar(varsvalue)#实际请求
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute('select reqparams,resparams from mock_config where status=0 and domain=%s and methods=%s',(domain, method))
        reqparams = cur.fetchall()
        for i in range(len(reqparams)):
            varsvalue2=reqparams[i][0] #数据库中的预期请求
            arr = varsvalue2.split('&')
            for i in range(len(arr)):
                arr[i] = arr[i] + '&'
            arr.sort(reverse=True)
            str = ''.join(arr)[0:-1]
            if str==varsvalue1:
                return reqparams[i-1][1].encode("utf-8")
            if reqparams[i][0] == '':
                return jsonify({"msg": "对应请求没有配置预期返回值"})
            else:
                return jsonify({"msg": "请求方法和参数不匹配"})


def getvar(value):
    value=value[::-1]
    result = ''
    f = 0
    for i in range(len(value)):
        for j in range(len(value[i])):
            if f % 2 == 0:
                result = result + value[i][j] + '='
                f = f + 1
            else:
                result = result + value[i][j] + '&'
                f = f + 1
    return result[0:-1]

def getre(path,varsvalue):
    r = checkpath(path, varsvalue, request.method)
    return r

@app.route('/<path:path>/<path:path1>', methods=['GET','POST'])
def get_all_task(path,path1):
    npath='/' + path + '/' + path1
    if request.method=='GET':
        varsvalue = request.args.items()
    else:
        varsvalue = request.form.items()
    r=getre(npath,varsvalue)
    return r

@app.route('/<path:path>', methods=['GET','POST'])
def get_all_task1(path):
    if request.method=='GET':
        varsvalue = request.args.items()
    else:
        varsvalue = request.form.items()
    r = getre(path, varsvalue)
    return r

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5201,threaded=True)