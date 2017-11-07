# -*- coding: utf-8 -*-
from flask import jsonify, Flask,make_response,request
import sys,ConfigParser
from flask_sqlalchemy import SQLAlchemy
reload(sys)
sys.setdefaultencoding('utf-8')

def getconfig():
    cf = ConfigParser.ConfigParser()
    path = 'db.config'
    cf.read(path)
    _dburi = cf.get("database","dbhost")
    return _dburi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getconfig()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class mock_config(db.Model):
    """定义数据模型"""
    __tablename__ = 'mock_config'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    reqparams = db.Column(db.String(500))
    methods = db.Column(db.String(50))
    domain = db.Column(db.String(50))
    description = db.Column(db.String(50))
    resparams = db.Column(db.String(500))
    update_time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Integer)
    ischeck = db.Column(db.Integer)
    project_name = db.Column(db.String(20))

def checksize(domain,method):
    mock = mock_config.query.filter_by(domain=domain).first()# 校验domain是否存在
    mock1 = mock_config.query.filter(mock_config.domain == domain,mock_config.methods == method).first() # 校验method是否存在
    if  not mock :
        return jsonify({"msg": u"请求方法不存在"})
    elif not mock1 :
        return jsonify({"msg": u"请求方法对应的请求模式不存在"})

def checkpath(domain,varsvalue,method):
    method=method.lower()
    varsvalue.sort()
    re=checksize(domain,method)#判断请求方法和模式是否匹配
    if re != None:
        return re
    if len(varsvalue) == 0:
        mock_data = mock_config.query.filter(mock_config.methods == method,mock_config.status ==0,mock_config.domain ==domain).first()
        resparams=mock_data.resparams
        if resparams== '':
            return jsonify({"msg": u"对应请求没有配置预期返回值"})
        else:
            return resparams.encode("utf-8")
    else:
        varsvalue1=getvar(varsvalue)
        mock_data = mock_config.query.filter(mock_config.methods == method, mock_config.status == 0,
                                             mock_config.domain == domain).first()
        if not varsvalue1:
            return jsonify({"msg": u"请求方法和参数不匹配"})
        elif mock_data.ischeck==1:
            return mock_data.resparams
        else:
            rdata=checkparams(mock_data,varsvalue1)
        return rdata

def checkparams(mock_data,varsvalue1):
    varsvalue2 = mock_data.reqparams  # 数据库中的预期请求参数
    if mock_data.methods.lower()=='get' or (mock_data.reqparams.lower()=='post' and varsvalue1[0] != '}' and varsvalue1[-2] != '}'):
        arr = varsvalue2.split('&')
        for i in range(len(arr)):
            arr[i] = arr[i] + '&'
        arr.sort(reverse=True)
        str = ''.join(arr)[0:-1]
        if str==varsvalue1 and mock_data.resparams != '':
            return mock_data.resparams.encode("utf-8")
        elif mock_data.resparams == '':
            return jsonify({"msg": u"对应请求没有配置预期返回值"})
        else:
            return jsonify({"msg": u"请求方法和参数不匹配"})
    elif mock_data.methods.lower()=='post':
        varsvalue1 = varsvalue1.replace("\t", "").replace("\r", "").strip()[:-1]
        varsvalue2 = varsvalue2.replace("\t", "").replace("\r", "").strip()
        if varsvalue1 == varsvalue2:
            return mock_data.resparams.encode("utf-8")
    else:
        return jsonify({"msg": u"暂不支持该类型请求方法"})

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

@app.route('/<path:path>/<path:path1>', methods=['GET','POST'])
def get_all_task(path,path1):
    npath='/' + path + '/' + path1
    if request.method=='GET':
        varsvalue = request.args.items()
    else:
        varsvalue = request.form.items()
    r = checkpath(npath, varsvalue, request.method)
    return r

@app.route('/<path:path>', methods=['GET','POST'])
def get_all_task1(path):
    path='/'+path
    if request.method=='GET':
        varsvalue = request.args.items()
    else:
        varsvalue = request.form.items()
    r = checkpath(path, varsvalue, request.method)
    return r

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(u"程序报错，可能是因为叙利亚战争导致", 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5201,threaded=True)
