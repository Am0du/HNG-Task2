import os

from flask import Flask, jsonify, request, redirect, url_for
from model import db, TaskTwo
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import bleach
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('key')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('postgres')
db.init_app(app)
with app.app_context():
    db.create_all()

def checker(name):
    word_list = list(name)
    checker = None
    for i in word_list:
        try:
            value = int(i)
        except ValueError:
            checker = True
        else:
            checker = False
            break
    return checker

@app.route('/')
def home():
    return jsonify(response='hey')

@app.route('/api', methods=['POST', 'PUT', 'GET', 'DELETE'])
def api():
    name = request.args.get('name')
    if checker(name):
        name = bleach.clean(name)
        if request.method == 'GET':
            return redirect(url_for('read', name=name)), 307
        elif request.method == 'POST':
            return redirect(url_for('create', name=name)), 307
        elif request.method == 'PUT':
            new_name = request.args.get('new_name')
            if checker(new_name):
                bleach_name = bleach.clean(new_name)
                return redirect(url_for('put', name=name, new_name=bleach_name)), 307
            else:
                return jsonify(response=f'{new_name} has a integer', status_code=400), 400

        elif request.method == 'DELETE':
            return redirect(url_for('delete', name=name)), 307
    else:
        return jsonify(response=f'{name} has a integer', status_code=400), 400

@app.route('/api/read', methods=['GET'])
def read():
    name = request.args.get('name')
    try:
        user = db.session.execute(db.select(TaskTwo).filter_by(name=name)).scalar_one()
    except NoResultFound:
        return jsonify(response='No Result Found', status_code=400), 400
    else:
        return jsonify(id=user.id, name=user.name), 200

@app.route('/api/create', methods=['POST'])
def create():
    name = request.args.get('name')
    try:
        user = TaskTwo(name=name)
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        return jsonify(response='This name already Exist', status_code=400), 400
    else:
        return jsonify(response=f'{name} created successfully', status_code=200), 200


@app.route('/api/put', methods=['PUT'])
def put():
    name = request.args.get('name')
    new_name = request.args.get('new_name')
    try:
        user = db.session.execute(db.select(TaskTwo).filter_by(name=name)).scalar_one()
    except NoResultFound:
        new_user = TaskTwo(name=new_name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(response=f'{new_name} have been found', status_code=400), 400
    else:
        user.name = new_name
        db.session.commit()
        return jsonify(response=f'{name} has been updated to {new_name}', status_code=200), 200


@app.route('/api/delete', methods=['DELETE'])
def delete():
    name = request.args.get('name')
    try:
        user = db.session.execute(db.select(TaskTwo).filter_by(name=name)).scalar_one()
    except NoResultFound:
        return jsonify(response=f'{name} does not exist', status_code=400), 400
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify(response=f'{name} has been deleted', status_code=200), 200

if __name__ == '__main__':
    app.run(debug=True)
