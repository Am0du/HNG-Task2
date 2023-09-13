import os

from flask import Flask, jsonify, request, redirect, url_for
from model import db, TaskTwo
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import bleach
import os
from random import randint

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
@app.route('/api/<int:id>', methods=['GET'])
def read(id):
    # name = request.form.get('name')
    try:
        user = db.session.execute(db.select(TaskTwo).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify(response=f'No Result with id={id} Found'), 404
    else:
        return jsonify(id=user.id, name=user.name, username=user.username), 200

@app.route('/api', methods=['GET'])
def home():
    users = db.session.execute(db.select(TaskTwo).order_by(TaskTwo.id)).scalars()
    list = []
    for user in users:
        data = {
            'id': user.id,
            'name': user.name,
            'username': user.name
        }
        list.append(data)

    return jsonify(response=list), 200

    return
@app.route('/api', methods=['POST'])
def create():
    data = request.get_json('name')
    name = data.get('name')
    random_int = randint(1, 1001)
    if checker(name):
        username = f'{name}{random_int}'
        user = TaskTwo(name=name, username=username)
        db.session.add(user)
        db.session.commit()
        user = db.session.execute(db.select(TaskTwo).filter_by(name=name)).scalar()
        return jsonify(response=f'{name} created successfully', id=user.id,
                       name=user.name, username=user.username), 201
    else:
        return jsonify(response=f'{name} contains an integer, not allowed', status_code=400), 400


@app.route('/api/<int:id>', methods=['PUT'])
def put(id):
    data = request.get_json('name')
    name = data.get('name')
    username = data.get('username')
    try:
        user = db.session.execute(db.select(TaskTwo).filter_by(id=id)).scalar_one()
    except NoResultFound:
        if checker(name):
            if username:
                username = username
            else:
                username = user.username
            user.name = name
            user.username = username
            user.username = user.username
            db.session.commit()
            updated = db.session.execute(db.select(TaskTwo).filter_by(id=id)).scalar()
            return jsonify(response='User update', id=updated.id, name=updated.name, username=updated.username,
                           status_code=201), 201
        return jsonify(response=f'user with id = {id} not found', status_code=404), 404
    else:
        if checker(name):
            if username:
                username = username
            else:
                username = user.username
            user.name = name
            user.username = username
            user.username = user.username
            db.session.commit()
            updated = db.session.execute(db.select(TaskTwo).filter_by(id=id)).scalar()
            return jsonify(response='User update', id=updated.id, name=updated.name, username=updated.username,
                           status_code=201), 201


@app.route('/api/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        user = db.session.execute(db.select(TaskTwo).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify(response=f'{id} does not exist', status_code=404), 404
    else:
        db.session.delete(user)
        db.session.commit()
        user = db.session.execute(db.select(TaskTwo).filter_by(id=id)).scalar()
        return jsonify(response=f'user with {user}has been deleted', status_code=204), 204

if __name__ == '__main__':
    app.run(debug=True)
