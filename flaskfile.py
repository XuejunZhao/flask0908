# coding: utf-8
import shelve
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import sqlite3, urllib, json, os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, escape, Markup, send_from_directory, make_response
from datetime import datetime
import os
from werkzeug import secure_filename,SharedDataMiddleware,generate_password_hash, check_password_hash
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flaskext.mysql import MySQL
from flask_cors import * #kuayu
from functools import wraps
import simplejson as json
import traceback
from collections import defaultdict
import database
import generator
import random
from config import APP_STATIC_TXT

app = Flask(__name__)


mysql = MySQL()


# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'd,tP<ujhw5ki'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# this will read in variables from config.py
app.config.from_object("config")
app.debug = True
CORS(app, supports_credentials=True)

tasks_test = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
  ]
tasks = [
      {
          "lng":116.368904,
          "lat":39.913423
      },
      {
          "lng":116.382122,
          "lat":39.90117
      },
      { 
          "lng":116.387271,
          "lat":39.912501
      },
      {
          "lng":116.368904,
          "lat":39.913423
      }   
    ]
tasks2 = {1:[
      {
          "lng":116.350000,
          "lat":39.913423
      },
      {
          "lng":116.382122,
          "lat":39.90117
      },
      { 
          "lng":116.387271,
          "lat":39.912501
      },
      {
          "lng":116.370000,
          "lat":39.913423
      }   
    ]}


# ====================================================================================
# setup and teardown for each HTTP request
# ====================================================================================
# the @ sign here means that app.before_request is a "decorator" for the function 
# defined in the next line. http://legacy.python.org/dev/peps/pep-0318/#current-syntax
# but you don't have to understand that to use it
#
# in a flask app, putting @app.before_request before a function means
# that this function will be called before a request is routed, and app.teardown_request
# is called after everything is finished.  
# So this is a good place to connect/disconnect to the database
@app.before_request
def before_request():
  g.dir = os.path.dirname(os.path.abspath(__file__))
  g.db  = sqlite3.connect(g.dir + '/' + app.config['DATABASE'])

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def print_exceptions(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception, e:
            print ''
            print '------'
            print 'API: exception'
            print e
            print traceback.format_exc()
            print request.url
            print request.data
            print '------'
            raise
    return wrapped
# ====================================================================================
# routes - these map URLs to your python functions
# ====================================================================================
def save_data(name, comment, create_at, first):
    """保存提交的数据
    """
    # 通过shelve模块打开数据库文件
    base = shelve.open(app.config['DATA_FILE'])
    # 如果数据库中没有greeting_list，就新建一个表
    if 'greeting_list' not in base:
        greeting_list = []
    else:
        # 从数据库获取数据
        greeting_list = base['greeting_list']
    # 将提交的数据添加到表头
    greeting_list.insert(0, {
        'name': name,
        'first': first,
        'comment': comment,
        'create_at': create_at,
    })
    # 更新数据库
    base['greeting_list'] = greeting_list
    # 关闭数据库文件
    base.close()

def load_data():
  """ 返回已提交的数据
  """
  # 通过shelve模块打开数据库文件
  base = shelve.open(app.config['DATA_FILE'])
  # 返回greeting_list。如果没有数据则返回空表 
  greeting_list = base.get('greeting_list', []) 
  base.close()
  print greeting_list
  return greeting_list

@app.route('/post', methods=['POST'])
def post():
    """用于提交评论的URL
    """
    # 获取已提交的数据
    name = request.form.get('name')  # 名字
    comment = request.form.get('comment')  # 留言
    first = request.form.get('first') 
    create_at = datetime.now()  # 投稿时间（当前时间）
    # 保存数据
    save_data(name, comment, create_at, first)
    # 保存后重定向到首页
    return redirect('/form')

def load_first(num):
  base = shelve.open(app.config['DATA_FILE'])
  first_list = base.get('first_list', [])[:num]
  base.close()
  return first_list

def load_second(num):
  base = shelve.open(app.config['DATA_FILE'])
  second_list = base.get('second_list', [])[:num]
  base.close()
  return second_list

def save_table(num):
    """保存提交的数据
    """
    # 通过shelve模块打开数据库文件
    base = shelve.open(app.config['DATA_FILE'])
    # 如果数据库中没有greeting_list，就新建一个表
    if 'first_table' not in base:
        first_table = []
    else:
        # 从数据库获取数据
        first_table = base['first_table']
    # 将提交的数据添加到表头
    first_table.insert(0, {
        'table_range': num,
    })
    # 更新数据库
    base['first_table'] = first_table

    base.close()

@app.route('/postfirst', methods=['POST'])
def postfirst():
    """用于提交评论的URL
    """
    # 获取已提交的数据
    table_range = request.form.get('first')
    save_table(int(table_range))
    return redirect('/graph')

@app.route('/graph')
def graph():
  base = shelve.open(app.config['DATA_FILE'])
  table_range = base.get('first_table', [])[0]['table_range']
  original_list = load_first(table_range) 
  sec_list =  load_second(table_range)
  # print table_range
  return render_template('data_prior.html', original_list = original_list, sec_list = sec_list)

dict_tem = {1:"上车",0:"下车"}
@app.template_filter('nl2br')
def nl2br_filter(j):
    """将换行符置换为br标签的模板过滤器
    """
    s=int(j)

    if s in dict_tem:
      # print dict_tem[s]
      return dict_tem[s]

@app.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    """使datetime对象更容易分辨的模板过滤器
    """
    return dt.strftime('%Y/%m/%d %H:%M:%S')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  flash('New entry was successfully posted')
  return redirect(url_for('table'))

@app.route('/rfm')
def rfm():
  return render_template("rfm.html")

@app.route('/form')#, methods=['GET', 'POST']
def form():
  greeting_list = load_data() 
  return render_template('form.html', greeting_list = greeting_list)

@app.route('/table')
def table():
  cur = g.db.execute('select title, text, mood, lat, long from entries order by id desc')
  entries = cur.fetchall()
  return render_template('table.html', entries=entries)

@app.route("/data", methods=["POST"])
@print_exceptions
def post_data():
    data = json.loads(request.data)
    for item in data:
        database.put(item)
    return jsonify({'result': 'OK', 'len': len(data)})


@app.route("/data", methods=["GET"])
@print_exceptions
def get_data():
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    result = database.find_if(
        lambda item:
            (not start or (start and item['ts'] >= int(start))) and
            (not end or (end and item['ts'] <= int(end)))
    )
    return jsonify({'data': result})


@app.route("/data/count", methods=["GET"])
@print_exceptions
def get_data_count():
    # data = database.find_if(lambda item: True)
    # result = defaultdict(int)
    # for item in data:
    #     ts_datetime = datetime.utcfromtimestamp(item['ts'])
    #     result[ts_datetime.strftime('%Y/%m/%d %H')] += 1
    result = {
    "2014-08-24":25498,
    "2014-08-25":7983,
    "2014-08-26":24927,
    "2014-08-27":7176,
    "2014-08-28":27542,
    "2014-08-29":9016,
    "2014-09-30":7758,
    "2014-09-31":7368,
    "2014-09-01":6460,
    "2014-09-02":25504,
    "2014-09-03":8229,
    "2014-09-04":8021,
    "2014-09-05":24435,
    "2014-09-06":7454,
    "2014-09-07":7771,
    "2014-09-08":22883,
    "2014-09-09":7796,
    "2014-09-10":7225,
    "2014-09-11":8091,
    "2014-09-12":19318,
    "2014-09-13":8050,
    "2014-09-14":27996,
    "2014-09-15":7105,
    "2014-09-16":24186,
    "2014-09-17":27511,
    "2014-09-18":8583,
    "2014-09-19":5217,
    "2014-09-20":8418,
    "2014-09-21":24999,
    "2014-09-22":9099,
    "2014-09-23":4748,
    "2014-09-24":26850,
    "2014-09-25":8921,
    "2014-09-26":6485,
    "2014-09-27":3869,
    "2014-09-28":4184,
    "2014-09-29":3437,
    "2014-09-30":4310,
    "2014-10-01":3986,
    "2014-10-02":2374,
    "2014-10-03":1213,
    "2014-10-04":5930,
    "2014-10-05":4305,
    "2014-10-06":3781,
    "2014-10-07":2958,
    "2014-10-08":7867,
    "2014-10-09":26740,
    "2014-10-10":25336,
    "2014-10-11":8575,
    "2014-10-12":24812,
    "2014-10-13":26450,
    "2014-10-14":24568,
    "2014-10-15":7414,
    "2014-10-16":24327,
    "2014-10-17":6418,
    "2014-10-18":6613,
    "2014-10-19":7155,
    }
    return jsonify({'data': result})

@app.route("/data/count2", methods=["GET"])
@print_exceptions
def get_data_count2():
    # data = database.find_if(lambda item: True)
    # result = defaultdict(int)
    # for item in data:
    #     ts_datetime = datetime.utcfromtimestamp(item['ts'])
    #     result[ts_datetime.strftime('%Y/%m/%d %H')] += 1
    result = {
    "2015-08-24":25498,
    "2015-08-25":7983,
    "2015-08-26":24927,
    "2015-08-27":7176,
    "2015-08-28":27542,
    "2015-08-29":9016,
    "2015-09-30":7758,
    "2015-09-31":7368,
    "2015-09-01":6460,
    "2015-09-02":25504,
    "2015-09-03":8229,
    "2015-09-04":8021,
    "2015-09-05":24435,
    "2015-09-06":7454,
    "2015-09-07":7771,
    "2015-09-08":22883,
    "2015-09-09":7796,
    "2015-09-10":7225,
    "2015-09-11":8091,
    "2015-09-12":19318,
    "2015-09-13":8050,
    "2015-09-14":27996,
    "2015-09-15":7105,
    "2015-09-16":24186,
    "2015-09-17":27511,
    "2015-09-18":8583,
    "2015-09-19":5217,
    "2015-09-20":8418,
    "2015-09-21":24999,
    "2015-09-22":9099,
    "2015-09-23":4748,
    "2015-09-24":26850,
    "2015-09-25":8921,
    "2015-09-26":6485,
    "2015-09-27":3869,
    "2015-09-28":4184,
    "2015-09-29":3437,
    "2015-09-30":4310,
    "2015-10-01":3986,
    "2015-10-02":2374,
    "2015-10-03":1213,
    "2015-10-04":5930,
    "2015-10-05":4305,
    "2015-10-06":3781,
    "2015-10-07":2958,
    "2015-10-08":7867,
    "2015-10-09":6740,
    "2015-10-10":5336,
    "2015-10-11":575,
    "2015-10-12":4812,
    "2015-10-13":6450,
    "2015-10-14":4568,
    "2015-10-15":7414,
    "2015-10-16":24327,
    "2015-10-17":6418,
    "2015-10-18":6613,
    "2015-10-19":7155,
    }
    return jsonify({'data': result})
@app.route("/data/heatmap", methods=["GET"])
@print_exceptions
def get_data_heatmap():
    #
    # {
    #   floor1: [ {'x':10, 'y':20, 'count':5}, ... ]
    #   ...
    # }
    data = database.find_if(lambda item: True)
    result = defaultdict(dict)
    for item in data:
        heat_hash = str(item['position']['x']) + '|' + str(item['position']['y'])
        if heat_hash in result[item['floor']]:
            result[item['floor']][heat_hash]['count'] += 1
        else:
            result[item['floor']][heat_hash] = {
                'x': item['position']['x'],
                'y': item['position']['y'],
                'count': 1
            }
    final_result = {}
    for floor in result:
        final_result[floor] = result[floor].values()
    return jsonify({'data': final_result})

@app.route('/map', methods = [ "POST", "GET" ])
def map():
  last_list = load_data()
  print last_list
  #cur = g.db.execute('select title, text, mood, lat, long from entries order by id desc')
  #entries = cur.fetchall()
  #return render_template('map.html', entries=entries)
  return render_template('map.html', last_list = last_list[0])

@app.route("/forward", methods=['POST'])
def move_forward():
    #Moving forward code
    base = shelve.open(DATA_FILE)
    greeting_list = base.get('greeting_list', [])
    argv_range = greeting_list[0]['name']
    argv_radius = greeting_list[0]['comment']
    app.config['RANGE_ARGS'] = argv_range 
    app.config['RADIUS_ARGS'] = argv_radius 
    # app.config['SPARK_METHOD']
    os.system('sh /Users/xuejun/Downloads/flask-for-data-science-master/load.sh %d %d' %(int(argv_range),int(argv_radius)))
    forward_message = "Moving Forward..."
    return redirect('/map')



@app.route('/map_api')
def map_api():
  # busline = request.args.get('busline')
  # if not busline in ['B26', 'B54', 'B61', 'B69']:
  #   busline = 'B26'
  # url = 'http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s' % (app.config['MTA_KEY'], busline)
  # json_data = urllib.urlopen(url).read()
  # bus_data = json.loads( json_data )['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]
  # entries = []
  # if( not 'ErrorCondition' in bus_data.keys() ):
  #   bus_data = bus_data['VehicleActivity']
  #   for bus in bus_data:
  #     location = bus['MonitoredVehicleJourney']['VehicleLocation'] 
  #     entries.append( location )
  #   app.logger.info('Found %d busses on line %s' % (len(entries), busline))
  return render_template('map_api.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      session['username'] = request.form['username']
      flash('You were logged in as ' + session['username'])
      return redirect( url_for('index') )
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('index'))


@app.route('/tasks', methods=['GET'])
def get_tasks():
  with open(os.path.join(APP_STATIC_TXT, 'data.json')) as json_file:
      tasks2 = json.load(json_file)
  return jsonify(tasks2)

@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
  task = filter(lambda t: t['id'] == task_id, tasks_test)
  if len(task) == 0:
      abort(404)
  return jsonify({'tasks': task[0]})

@app.route('/task', methods=['POST','GET'])
def create_task():
    tasks2[len(tasks2)+1] = request.json
    return jsonify(request.json), 201

@app.route('/json', methods=['POST'])
def c_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
         len(tasks_test) + 1: request.json
        # 'title': request.json['title'],
        # 'description': request.json.get('description', ""),
        # 'done': False
    }
    tasks_test.append(request.get_data())
    tasks2[len(tasks2)+1] = request.json
    return jsonify(request.json), 201

@app.route('/monitor_test', methods=['GET', 'POST'])
def monitor_test():
    with open(os.path.join(APP_STATIC_TXT, '7.txt')) as f:
        s=f.readlines(5) #读取前五个字节
        f.close()
    return 'ok'+str(s)
# ====================================================================================
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

# ====================================================================================
if __name__ == '__main__':
  app.run()
# ====================================================================================
