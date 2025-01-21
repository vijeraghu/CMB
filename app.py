# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    booker_name = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_availability', methods=['POST'])
def check_availability():
    data = request.json
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])
    
    # Check each vehicle's availability
    available_vehicles = []
    for vehicle_num in range(1, 4):  # Check vehicles 1, 2, and 3
        overlapping = Booking.query.filter(
            Booking.vehicle_number == vehicle_num,
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()
        
        if not overlapping:
            available_vehicles.append(vehicle_num)
    
    return jsonify({'available_vehicles': available_vehicles})

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    try:
        booking = Booking(
            vehicle_number=data['vehicle_number'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            booker_name=data['booker_name']
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({'message': 'Booking successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)