
# A very simple Flask Hello World app for you to get started with...
import os, datetime
from pony.orm import *
from flask import Flask, request, render_template, session, redirect

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

db.bind(provider='sqlite', filename='data.db', create_db=True)
sql_debug(True)
db.generate_mapping(create_tables=True)

@db_session
def add_people(params):
    People(**params)

@db_session
def lookup():
    ps = People.select().order_by(desc(People.reg_date))[:10]
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
        if not 'src_address' in params:
            session['info'] = '信息填写不完整，请重新填写！'
            return redirect('/')
        else:
            add_people(params)
            return render_template('success.html')

@app.route('/dis')
def display():
    peoples = lookup()
    return render_template('display.html', peoples=peoples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')