from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # or another database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Plant

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200

@app.route('/plants', methods=['POST'])
def create_plant():
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    name = data.get('name')
    image = data.get('image')
    price = data.get('price')

    if not name or not image or not price:
        abort(400, description="Missing required fields")

    new_plant = Plant(name=name, image=image, price=price)
    db.session.add(new_plant)
    db.session.commit()

    return jsonify(new_plant.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
