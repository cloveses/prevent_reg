
# A very simple Flask Hello World app for you to get started with...
import os, datetime
from pony.orm import *
from flask import Flask, request, render_template, session, redirect, jsonify

app = Flask(__name__)
app.secret_key = 'abck&&&((%^%^jjjhhku76993KJH'

db = Database()
class People(db.Entity):
    name = Optional(str)
    idcode = Optional(str)
    address = Required(str)
    phone = Optional(str)
    src_address = Optional(str)
    back_date = Optional(str)
    is_fever = Optional(str)
    memo = Optional(str)
    reg_date = Required(datetime.datetime, default=datetime.datetime.now)

class SecPeople(db.Entity):
    work_place = Required(str)
    name = Required(str)
    sex = Required(str)
    education = Required(str)
    idcode = Required(str)
    phone = Required(str)
    politic = Required(str)
    occupation = Required(int)
    other = Required(int)
    memo = Optional(str)
    reg_date = Required(datetime.datetime, default=datetime.datetime.now)

class Talent(db.Entity):
    headname = Required(str)
    relation = Required(str)
    relation_name = Required(str)
    sex = Required(str)
    age = Required(int)
    address = Required(str)
    work_place = Required(str)
    phone = Required(str)
    info = Required(str)
    memo = Optional(str)
    reg_date = Required(datetime.datetime, default=datetime.datetime.now)

db.bind(provider='sqlite', filename='data.db', create_db=True)
sql_debug(True)
db.generate_mapping(create_tables=True)

@db_session
def add_people(params):
    People(**params)

@db_session
def add_sec_people(params):
    SecPeople(**params)

@db_session
def lookup():
    ps = People.select().order_by(desc(People.reg_date))[:10]
    if ps:
        return [p.to_dict() for p in ps]
    return []

@db_session
def lookup_sec_people():
    ps = SecPeople.select().order_by(desc(SecPeople.reg_date))[:10]
    if ps:
        return [p.to_dict() for p in ps]
    return []


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        info = ''
        if 'info' in session:
            info = session['info']
            session.pop('info')
        return render_template('index.html', info=info)
    else:
        params = {}
        keys = ('name', 'idcode', 'address', 'phone',
            'src_address', 'back_date', 'is_fever', 'memo')
        for key in keys:
            v = request.form.get(key, '').strip()
            # print(key, v)
            if v:
                params[key] = v
        # print(params)
        if not 'address' in params:
            session['info'] = '信息填写不完整，请重新填写！'
            return redirect('/')
        else:
            add_people(params)
            return render_template('success.html')

@app.route('/dis')
def display():
    peoples = lookup()
    return render_template('display.html', peoples=peoples)

@app.route('/s')
def displaysec():
    peoples = lookup_sec_people()
    return render_template('display_sec.html', peoples=peoples)


@app.route('/second', methods=['GET', 'POST'])
def second():
    if request.method == 'GET':
        info = ''
        if 'info' in session:
            info = session['info']
            session.pop('info')
        return render_template('second.html', info=info)
    else:
        keys = ('work_place', 'name', 'education','idcode',
            'phone', 'politic', 'occupation', 'other', 'memo')
        params = {}
        for key in keys:
            v = request.form.get(key, '').strip()
            # print(key, v)
            if v:
                params[key] = v
        if ('memo' in keys and len(params) >= 9) or len(params) >= 8 and params['idcode'][-2].isdigit():
            sex = int(params['idcode'][-2])
            params['sex'] = '男' if sex % 2 == 1 else '女'
            add_sec_people(params)
            return jsonify(status=0, msg='谢谢合作!')
        else:
            return jsonify(status=1, msg=params['name'] + ' 填写不完整')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')