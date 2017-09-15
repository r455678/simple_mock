#coding=utf-8
from flask import Flask,request,jsonify,make_response
import requests,os
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app=Flask(__name__)
url ='http://192.168.20.154'
filename='case.xls'

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

def getres(request,npath):
    varsvalue = request.args.items()
    params = getvar(varsvalue)
    url1 = url + npath + '?'
    if request.method == 'GET':
        re = requests.get(url1, params=params)
    else:
        re = requests.post(url1, params=params)
    return re,params

def saveexcel(path,method,reqparams,resparams):
    book = Workbook()
    if os.path.exists(filename):
        resparams = resparams.decode('utf-8')
        writeexcel(path, method, reqparams ,resparams,u'false')
    else:
        sheet1 = book.add_sheet('Sheet 1')
        data=[u'用例名称',u'接口地址',u'请求方法',u'请求参数',u'预期结果', u'是否检查数据库', u'SQL语句', u'SQL预期结果']
        for i in range(0, len(data)):
            sheet1.write(0, i, data[i])
        book.save(filename)
        writeexcel(path, method, reqparams, resparams, u'false')

def writeexcel(data0,data1,data2,data3,data4):
    rexcel = open_workbook(filename)
    rows = rexcel.sheets()[0].nrows
    excel = copy(rexcel)
    table = excel.get_sheet(0)
    table.write(rows, 1, data0)
    table.write(rows, 2, data1)
    table.write(rows, 3, data2)
    table.write(rows, 4, data3)
    table.write(rows, 5, data4)
    for i in range(0, 8):
        table.col(i).width = 256 * 35
    excel.save(filename)

@app.route('/<path:path>/<path:path1>', methods=['GET','POST'])
def get_all_task(path,path1):
    npath='/' + path + '/' + path1
    re=getres(request,npath)
    saveexcel(npath, request.method,re[1],re[0].content)
    return re[0].content

@app.route('/<path:path>', methods=['GET','POST'])
def get_all_task1(path):
    path ='/'+path
    re = getres(request, path)
    saveexcel(path, request.method, re[1], re[0].content)
    return re[0].content

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 page Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True,port=5202)

