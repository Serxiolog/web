from flask import Flask, request, render_template, redirect, session
from data import db_session
from data.product import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


secret = 'dwJG8OTtU7J5TQDBrdj88RBSThj91P'
app = Flask(__name__)
db_session.global_init("db/project.sqlite")
db = db_session.create_session()
engine = create_engine('sqlite:///db/project.sqlite', echo=True)
Session = sessionmaker(bind=engine)
sessions = Session()


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def check():
    return redirect('/main')


@app.route('/main', methods=['POST', "GET"])
def magaz():
    if not session.get('cart'):
        session['cart'] = []
    items = db.query(Products).all()
    if request.method == "POST":
        count = request.form['count']
        id = request.form['id']
        price = request.form['price']
        name = request.form['name']
        if count:
            if len(session['cart']) != 0:
                session['cart'] += [{
                    'id' : id,
                    'count' : count,
                    'j' : session['cart'][-1]['j'] + 1,
                    'price' : price,
                    'name' : name,
                    'on' : int(count) * int(price)
                }]
            else:
                session['cart'] += [{
                    'id' : id,
                    'count' : count,
                    'j' : 0,
                    'price' : price,
                    'name' : name,
                    'on': int(count) * int(price)
                }]
        return render_template('main.html', title='title', data=items)
    else:
        return render_template('main.html', title='title', data=items)


@app.route('/add', methods=["POST", "GET"])
def add_item():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        check_password = request.form['password']
        if check_password != secret:
            print('bad')
            return render_template('add.html', title='title')
        item = Products(name = title, price = price)
        try:
            sessions.add(item)
            sessions.commit()
            return redirect('/main')
        except Exception:
            return render_template('add.html')
    return render_template('add.html')


@app.route('/checker', methods=["POST", "GET"])
def checker():
    if not session.get('cart'):
        session['cart'] = []
    add = session['cart']
    summ = 0
    for i in add:
        summ += i['on']
    if request.method == 'POST':
        name = request.form['firstName']
        surname = request.form['lastName']
        email = request.form['email']
        address = request.form['address']
        session['cart'] = []
        return render_template('send.html', data=add, name=name, surname=surname, add=summ, address=address, email=email)
    return render_template('checker.html', data=add, add=summ)


@app.route('/bag', methods=["POST", "GET"])
def bag():
    if not session.get('cart'):
        session['cart'] = []
    add = session['cart']
    data = []
    for j, i in enumerate(add):
        data.append({
            'id' : i['id'],
            'j' : i['j'],
            'count' : i['count'],
            'name' : i['name'],
            'price' : i['price'],
            'on' : i['on']
        })
    if request.method == 'POST':
        id = request.form['id']
        print(data)
        for i in range(len(data)):
            if str(data[i]['id']) == str(id):
                _ = data.pop(i)
                session['cart'] = data
                break

    return render_template('bag.html', data=data)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
