from flask import request, make_response, abort, jsonify 
from datetime import datetime as dt
from flask import current_app as app
import sqlalchemy as db
from sqlalchemy import and_, or_
from .models import db, Drone, DroneSchema, Medication, DroneMeds
import re



@app.route('/drone/add', methods=['POST'])
def add_drone_data():
    data                  = request.get_json()
    data_serial_no        = data['serial_no']
    data_model            = data['model']
    data_weight           = data['weight']
    data_battery_capacity = data['battery_capacity']

    if data_serial_no and data_model and data_weight and data_battery_capacity:
        existing_drone = (Drone.query.filter(Drone.serial_no == data_serial_no).one_or_none())

        if existing_drone is None:
            if data_battery_capacity > 25:
                if data_weight > 0 and data_weight < 500:
                    new_drone = Drone(
                        serial_no        = data_serial_no,
                        model            = data_model,
                        weight           = data_weight,
                        battery_capacity = data_battery_capacity
                    )
                    db.session.add(new_drone)
                    db.session.commit()
                    response = { 'message': 'Drone added successfully.'}
                else:
                    response = { 'message': 'Weight unacceptable.'}
            else:
                response = { 'message': 'Not enough battery capacity.'}
        else:
            response = { 'message': f'Serial Number: {data_serial_no} already exists.'}
    else:
        response = { 'message': 'Incomplete data'}

            
    return make_response(jsonify(response), 400)

@app.route('/medication/add', methods=['POST'])
def add_medication_data():
    data        = request.get_json()
    data_name   = data['name']
    data_code   = data['code']
    data_weight = data['weight']
    data_image  = data['image']

    if data_name and data_code and data_weight and data_image:
        existing_medication = (Medication.query.filter(Medication.code == data_code).one_or_none())

        if existing_medication is None:
            if re.match("^[a-zA-Z0-9_-]+$", data_name):
                if re.match("^[A-Z0-9_*]+$", data_code):
                    new_meds = Medication(
                        code   = data_code,
                        name   = data_name,
                        weight = data_weight,
                        image  = data_image
                    )
                    db.session.add(new_meds)
                    db.session.commit()
                    response = { 'message': 'Medication added successfully.'}
                else:
                    response = { 'message': 'Incorrect code. Only uppercase alphanumeric charecters, and "_" are allowed.'}
            else:
                response = { 'message': 'Incorrect name. Only alphanumeric charecters, "-" and "_" are allowed.'}
        else:
            response = { 'message': f'Medication code: {existing_medication} already exists.'}
    else:
        response = { 'message': 'Incomplete data'}

            
    return make_response(jsonify(response), 400)

@app.route('/drone/available', methods=['GET'])
def check_drone_availability():
    data = {}
    available_drones = (Drone.query.filter(
        or_(
            Drone.state == 'IDLE',
            Drone.state == 'LOADING'))
        ).all()

    if available_drones is not None:
        for records in available_drones:
            data[records.id] = records
        response = data
    else:
        response = { 'message': 'No drones available.'}

    return make_response(jsonify(response), 400)

@app.route('/drone/battery-check/<serialno>', methods=['GET'])
def check_drone_battery_level(serialno):
    the_drone = (Drone.query.filter(
            Drone.serial_no == serialno)
        ).first()

    if the_drone is not None:
        response = { 'drone' : the_drone }
    else:
        response = { 'message': 'No such drone.'}

    return make_response(jsonify(response), 400)

@app.route('/add-medications', methods=['POST'])
def add_meds_to_drone():
    data           = request.get_json()
    data_serial_no = data['serial_no']
    data_code      = data['code']

    if data_serial_no and data_code:
        med_added = DroneMeds(
            code      = data_code,
            serial_no = data_serial_no
        )
        db.session.add(med_added)
        db.session.commit()
        response = { 'message': 'Medication added successfully to drone.'}
    else:
        response = { 'message': 'Incomplete data'}

            
    return make_response(jsonify(response), 400)

    
