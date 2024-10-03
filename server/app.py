#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_items = Bakery.query.all()
    response = [item.to_dict() for item in bakery_items]

    return make_response(jsonify(response), 200)
    


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_item = Bakery.query.filter_by(id = id).first()
    if bakery_item:
        response = bakery_item.to_dict()
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify({"error": "Bakery not found"}))


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakery_item = BakedGood.query.order_by(BakedGood.price.desc()).all()
    if bakery_item:
        response = [item.to_dict() for item in bakery_item]
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify({"error": "Price is not avaialble"}), 400)
    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bakery_item = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bakery_item:
        response = bakery_item.to_dict()
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify({"error": "Price is not avaialble"}), 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
