#coding=utf-8
from  flask import Flask,request,jsonify,make_response,abort
from flask_cors import *
import pymysql,xlrd
from flask_restful import reqparse
from datetime import datetime
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

save_path=_path
ALLOWED_EXTENSIONS = ['xls', 'xlsx']
app=Flask(__name__)
CORS(app, supports_credentials=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/import_excel', methods=[ 'POST'])
def import_device():
    file = request.files['files[]']
    filename = file.filename
    # 判断文件名是否合规
    if file and allowed_file(filename):
        file.save(save_path+filename)
        excelName = save_path+filename
        bk = xlrd.open_workbook(excelName, encoding_override="utf-8")
        sh = bk.sheets()[0]  # 因为Excel里只有sheet1有数据，如果都有可以使用注释掉的语句
        ncols = sh.ncols#列
        nrows = sh.nrows#行
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        for j in range(1,nrows):
            if j+1 == nrows:
                return jsonify({'msg': "ok", "remark": "上传成功"})
            else:
                lvalues = sh.row_values(j+1)
                if lvalues[6]=='是':
                    ischeck = 0
                elif lvalues[6]=='否':
                    ischeck = 1
                else :
                    ischeck = 1
                try:
                    cur.execute('insert into mock_config values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(None,lvalues[0],lvalues[4],lvalues[3],lvalues[2],lvalues[7],lvalues[5],datetime.now(),0,ischeck,lvalues[1]))
                    conn.commit()
                except:
                    return jsonify({'msg': "fail", "remark": "解析失败"})
        conn.close()
        return jsonify({'msg': "ok", "remark": "上传成功"})
    else:
        return jsonify({'msg': "fail", "remark": "上传文件不符合格式要求"})

@app.route('/addinfo',methods=['POST'])
def query_user():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str,required=True)
    parser.add_argument('method', type=str,required=True)
    parser.add_argument('reqparams', type=str, required=True)
    parser.add_argument('resparams', type=str, required=True)
    parser.add_argument('des', type=str)
    parser.add_argument('domain', type=str,required=True)
    parser.add_argument('projectName', type=str,required=True)
    parser.add_argument('ischeck', type=int, required=True)
    args = parser.parse_args()
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('insert into mock_config (title,reqparams,methods,domain,description,resparams,status,ischeck,project_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ',(args.get('title'),args.get('reqparams'),args.get('method'),args.get('domain'),args.get('des'),args.get('resparams'), 0 , args.get('ischeck'),args.get('projectName')))
        conn.commit()
        conn.close()
    except :
        return jsonify({'msg': "fail", "remark": "新增数据失败"})
    return jsonify({'msg': "ok","remark":""})

@app.route('/delinfo',methods=['POST'])
def delinfo():
    parser = reqparse.RequestParser()
    parser.add_argument('id[]', type=str, required=True,action='append')
    args = parser.parse_args()
    id=args.get('id[]')
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        for index in range(len(id)):
            idd=id[index]
            cur.execute('delete from mock_config where id=%s',(idd))
        conn.commit()
        conn.close()
    except :
        return jsonify({'msg': "fail", "remark": "删除数据失败"})
    return jsonify({'msg': "ok","remark":""})

@app.route('/editinfo',methods=['POST'])
def editinfo():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('method', type=str, required=True)
    parser.add_argument('reqparams', type=str, required=True)
    parser.add_argument('resparams', type=str, required=True)
    parser.add_argument('des', type=str)
    parser.add_argument('domain', type=str, required=True)
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('projectName', type=str, required=True)
    parser.add_argument('ischeck', type=int, required=True)
    args = parser.parse_args()
    try:
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute('update mock_config set title=%s,reqparams=%s,methods=%s,domain=%s,description=%s,resparams=%s,update_time=%s ,project_name=%s ,ischeck=%s'
                    ' where id=%s',(args.get('title'),args.get('reqparams'),args.get('method'),args.get('domain'), args.get('des'), args.get('resparams'),
                                   datetime.now().strftime('%y-%m-%d %H:%M:%S'),args.get('projectName'),args.get('ischeck'),args.get('id')))
        conn.commit()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "编辑数据失败"})
    return jsonify({'msg': "ok", "remark": ""})

@app.route('/selectinfo',methods=['GET'])
def selectinfo():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    args = parser.parse_args()
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('select title,reqparams,methods,domain,description,resparams,project_name,ischeck from mock_config where id=%s',(args.get('id')))
        re= cur.fetchall()
        conn.close()
        key = ('title', 'reqparams', 'methods', 'domain', 'description', 'resparams','project_name','ischeck')
        d = [dict(zip(key, value)) for value in re]
    except:
        return jsonify({'msg': "fail", "remark": "查询信息失败"})
    return jsonify({'msg': "ok", "remark": "", 'data':d})

@app.route('/manage',methods=['POST'])
def manage():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('status', type=int, required=True)
    args = parser.parse_args()
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute('update mock_config set status=%s where id=%s',(args.get('status'),args.get('id')))
        conn.commit()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "查询信息失败"})
    return jsonify({'msg': "ok", "remark": ""})

@app.route('/search',methods=['GET'])
def search():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('project_name', type=str, required=True)
    args = parser.parse_args()
    try:
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        if args.get('project_name') == str(0):
            sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s') from mock_config where title like %s"
            value=args.get('title').strip()
            cur.execute(sql, value+'%%')
        else:
            sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s') from mock_config where title like %s and project_name=%s"
            values = (args.get('title')+'%%' .strip(),args.get('project_name'))
            cur.execute(sql,values)
        re= cur.fetchall()
        conn.close()
        key = ('id','status','title', 'reqparams', 'methods', 'domain', 'description', 'resparams','updateTime')
        d = [dict(zip(key, value)) for value in re]
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "", "data": d})

@app.route('/searchall',methods=['GET'])
def searchall():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute("select id,title,reqparams,methods,domain,description,resparams,status,date_format(update_time,'%Y-%m-%d %H:%i:%s') from mock_config")
        re= cur.fetchall()
        conn.close()
        key = ('id','title', 'reqparams', 'methods', 'domain', 'description', 'resparams','status','updateTime')
        d = [dict(zip(key, value)) for value in re]
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": d})

@app.route('/searchproject',methods=['GET'])
def searchproject():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT(project_name) from mock_config")
        re= cur.fetchall()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": "","data": re})

@app.route('/copy',methods=['POST'])
def copy():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    args = parser.parse_args()
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    try:
        cur.execute("insert into mock_config(title,reqparams,methods,domain,description,resparams,update_time,status,project_name,ischeck) "
                    "select title,reqparams,methods,domain,description,resparams,update_time,status,project_name,ischeck from mock_config where id=%s",args.get('id'))
        conn.commit()
        conn.close()
    except:
        return jsonify({'msg': "fail", "remark": "select data fail"})
    return jsonify({'msg': "ok", "remark": ""})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True,port=5202)