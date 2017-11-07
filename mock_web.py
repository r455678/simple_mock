#coding=utf-8
from  flask import Flask,request,jsonify,make_response
from flask_cors import *
from flask_restful import reqparse
from datetime import datetime
import sys,xlrd,mock_server
from flask_sqlalchemy import SQLAlchemy
reload(sys)
sys.setdefaultencoding('utf-8')

save_path='D:\\'
ALLOWED_EXTENSIONS = ['xls', 'xlsx']
app=Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = mock_server.getconfig()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
#app.config['SQLALCHEMY_ECHO']=True
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
        nrows = sh.nrows#行
        for j in range(1,nrows):
            if j+1 == nrows:
                return jsonify({'msg': "ok", "remark": "上传成功"})
            else:
                lvalues = sh.row_values(j+1)
                if lvalues[6]=='是':
                    ischeckr = 0
                elif lvalues[6]=='否':
                    ischeckr = 1
                else :
                    ischeckr = 1
                try:
                    mock = mock_config(id=None, title=lvalues[0], reqparams=lvalues[4],methods=lvalues[3], domain=lvalues[2],
                                       description=lvalues[7], resparams=lvalues[5], update_time=datetime.now(),
                                       status=0, ischeck=ischeckr, project_name=lvalues[1])
                    db.session.add(mock)
                    db.session.commit()
                except:
                    return jsonify({'msg': "fail", "remark": "解析失败"})
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
    try:
        mock=mock_config(id=None,title=args.get('title'),reqparams=args.get('reqparams'),methods=args.get('method'),domain=args.get('domain'),
                     description=args.get('des'),resparams=args.get('resparams'),update_time=None,status=0,ischeck=args.get('ischeck'),project_name=args.get('projectName'))
        db.session.add(mock)
        db.session.commit()
    except :
        return jsonify({'msg': "fail", "remark": "新增数据失败"})
    return jsonify({'msg': "ok","remark":""})

@app.route('/delinfo',methods=['POST'])
def delinfo():
    parser = reqparse.RequestParser()
    parser.add_argument('id[]', type=str, required=True,action='append')
    args = parser.parse_args()
    id=args.get('id[]')
    try:
        for index in range(len(id)):
            idd=id[index]
            mock=mock_config.query.filter_by(id=idd).first()
            db.session.delete(mock)
            db.session.commit()
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
        mock=mock_config.query.filter_by(id=args.get('id')).first()
        mock.title=args.get('title')
        mock.reqparams = args.get('reqparams')
        mock.methods = args.get('method')
        mock.description = args.get('des')
        mock.domain = args.get('domain')
        mock.projectName = args.get('projectName')
        mock.resparams = args.get('resparams')
        mock.project_name = args.get('projectName')
        mock.ischeck = args.get('ischeck')
        mock.update_time=datetime.now().strftime('%y-%m-%d %H:%M:%S')
        db.session.commit()
    except :
        return jsonify({'msg': "fail", "remark": "修改数据失败"})
    return jsonify({'msg': "ok", "remark": ""})

@app.route('/manage',methods=['POST'])
def manage():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('status', type=int, required=True)
    args = parser.parse_args()
    try:
        mock=mock_config.query.filter(mock_config.id == args.get('id') and mock_config.status == args.get('status')).first()
        mock.status=args.get('status')
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "修改数据失败"})
    return jsonify({'msg': "ok", "remark": ""})

@app.route('/search',methods=['GET'])
def search():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('project_name', type=str, required=True)
    args = parser.parse_args()
    if args.get('project_name') == str(0):
        conn = db.session.connection()
        sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s') from mock_config where title like %s"
        value = args.get('title').strip()
        re=conn.execute(sql, '%%'+ value + '%%')
        conn.close
    else:
        conn = db.session.connection()
        sql = "select id,status,title,reqparams,methods,domain,description,resparams,date_format(update_time,'%%Y-%%m-%%d %%H:%%i:%%s') from mock_config where title like %s and project_name=%s"
        values = ('%%'+args.get('title') + '%%'.strip(), args.get('project_name'))
        re=conn.execute(sql, values)
        conn.close
    key = ('id','status','title', 'reqparams', 'methods', 'domain', 'description', 'resparams','updateTime')
    d = [dict(zip(key, value)) for value in re]
    return jsonify({'msg': "ok", "remark": "", "data": d})

@app.route('/searchproject',methods=['GET'])
def searchproject():
    try:
        project_name = db.session.query(mock_config.project_name.distinct()).all()
    except:
        return jsonify({'msg': "fail", "remark": "查询项目数据失败"})
    return jsonify({'msg': "ok", "remark": "","data": project_name})

@app.route('/copy',methods=['POST'])
def copy():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    args = parser.parse_args()
    try:
        mock=mock_config.query.filter_by(id=args.get('id')).first()
        mock1=mock_config(id=None,title=mock.title,reqparams=mock.reqparams,methods=mock.methods,domain=mock.domain,description=mock.description
                            ,resparams=mock.resparams,update_time=mock.update_time,status=mock.update_time,ischeck=mock.ischeck,project_name=mock.project_name)
        db.session.add(mock1)
        db.session.commit()
    except:
        return jsonify({'msg': "fail", "remark": "复制项目数据失败"})
    return jsonify({'msg': "ok", "remark": ""})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg':'fail','error': '404 Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True,port=5202)
