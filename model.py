## 1️⃣ **app/__init__.py**

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import routes

## 2️⃣ **app/models.py**

from app import db

class IntrusionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_ip = db.Column(db.String(100), nullable=False)
    destination_ip = db.Column(db.String(100), nullable=False)
    attack_type = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

## 3️⃣ **app/routes.py**

from flask import request, jsonify
from app import app, db
from app.models import IntrusionLog
from datetime import datetime

@app.route('/logs', methods=['POST'])
def add_log():
    data = request.json
    new_log = IntrusionLog(
        source_ip=data['source_ip'],
    destination_ip=data['destination_ip'],
        attack_type=data['attack_type'],
        timestamp=datetime.utcnow()
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Intrusion log added successfully!'}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = IntrusionLog.query.all()
    return jsonify([{'id': log.id, 'source_ip': log.source_ip, 'destination_ip': log.destination_ip, 'attack_type': log.attack_type, 'timestamp': log.timestamp} for log in logs])

@app.route('/logs/<int:id>', methods=['DELETE'])
def delete_log(id):
    log = IntrusionLog.query.get(id)
    if not log:
        return jsonify({'message': 'Log not found'}), 404
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Log deleted successfully'})
