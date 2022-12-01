import os 
from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from models import db, Patient, Clinical_record, Caregiver, Drug, Control
from datetime import date, datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR,"final-project.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ENV"] = "development"
app.config["SECRET_KEY"] = "super_secret_key"
app.config["JWT_SECRET_KEY"] = "super_jwt_key"

db.init_app(app)
CORS(app)
Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.route("/")
def home():
    return "prueba exitosa"

@app.route("/login_patient", methods=["POST"])
def login_patient():
    password = request.json.get("password")
    rut = request.json.get("rut")

    found_patient = Patient.query.filter_by(rut=rut).first()

    if found_patient is None:
        return jsonify ({
            "msg": "no existen pacientes registrados con este rut"
        }), 404
    
    if bcrypt.check_password_hash(found_patient.password, password):
        access_token = create_access_token(identity=rut)
        return jsonify({
            "acess_token": access_token,
            "data": found_patient.serialize(),
            "success": True
        }), 200
    
    else:
        return jsonify ({
            "msg": "la contraseña es incorrecta"
        })


@app.route("/patient_list", methods=["GET"])
def patient_list():
    patient = Patient.query.all()
    patient_serialized = list(map( lambda patient: patient.serialize(), patient))
    return jsonify(patient_serialized)

@app.route("/add_patient", methods=["POST"])
def add_patient():
    patient = Patient()
    email = request.json.get("email")
    rut = request.json.get("rut")
    password = request.json.get("password")

    found_patient = Patient.query.filter_by(rut=rut).first()

    if found_patient is not None:
        return jsonify({
            "msg": "Ya existe un paciente ingresado con este rut"
        }), 400
    
    found_email = Patient.query.filter_by(email=email).first()

    if found_email is not None:
        return jsonify({
            "msg": "Ya existe un paciente ingresado con este email"
        }), 400

    patient.name = request.json.get("name")
    patient.lastname = request.json.get("lastname")
    patient.rut = rut
    patient.age = request.json.get("age")
    patient.gender = request.json.get("gender")
    patient.birth_date = request.json.get("birth_date")
    patient.email = email
    password_hash = bcrypt.generate_password_hash(password)
    patient.password = password_hash
    patient.address = request.json.get("address")
    patient.phone_number = request.json.get("phone_number")
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return jsonify({
        "msg": "paciente añadido correctamente"
        }), 200

@app.route("/update_patient/<int:id>", methods=["PUT"])
def update_patient(id):
    patient = Patient.query.get(id)
    patient.name = request.json.get("name")
    patient.lastname = request.json.get("lastname")
    patient.rut = request.json.get("rut")
    patient.age = request.json.get("age")
    patient.gender = request.json.get("gender")
    patient.birth_date = request.json.get("birth_date")
    patient.email = request.json.get("email")
    patient.password = request.json.get("password")
    patient.address = request.json.get("address")
    patient.phone_number = request.json.get("phone_number")
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return "paciente actualizado correctamente"

@app.route("/update_patient_alive/<int:id>", methods=["PUT"])
def update_patient_alive(id):
    patient = Patient.query.get(id)
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return "se ha cambiado el estado del paciente a fallecido"

@app.route("/delete_patient/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)
    
    db.session.delete(patient)
    db.session.commit()

    return "paciente eliminado correctamente"

@app.route("/get_caregiver", methods=["GET"])
def get_caregiver():
    caregiver = Caregiver.query.all()
    caregiver_serialized = list(map( lambda caregiver: caregiver.serialize(), caregiver))
    return jsonify(caregiver_serialized)

@app.route("/add_caregiver", methods=["POST"])
def add_caregiver():
    caregiver = Caregiver()
    patient_id = request.json.get("patient_id")

    found_patient = Patient.query.filter_by(id=patient_id).first()

    if found_patient is None:
        return jsonify({
            "msg": "no existe este paciente"
        }), 400

    found_caegiver = Caregiver.query.filter_by(patient_id=patient_id).first()

    if found_caegiver is not None:
        return jsonify({
            "msg": "este paciente ya tiene un cuidador asignado"
        }), 400

    caregiver.name = request.json.get("name")
    caregiver.lastname = request.json.get("lastname")
    caregiver.rut = request.json.get("rut")
    caregiver.address = request.json.get("address")
    caregiver.patient_id = patient_id

    db.session.add(caregiver)
    db.session.commit()

    return jsonify({
        "msg": "cuidador añadido correctamente"
    }), 200


@app.route("/get_clinical_record", methods=["GET"])
def get_clinical_record():
    clinical_record = Clinical_record.query.all()
    clinical_record_serialized = list(map( lambda clinical_record: clinical_record.serialize(), clinical_record))
    return jsonify(clinical_record_serialized)

@app.route("/create_clinical_record", methods=["POST"])
def create_clinical_record():
    clinical_record = Clinical_record()
    patient_id = request.json.get("patient_id")

    found_patient = Patient.query.filter_by(id=patient_id).first()

    if found_patient is None:
        return jsonify({
            "msg": "no existe este paciente"
        }), 400

    found_clinical_record = Clinical_record.query.filter_by(patient_id=patient_id).first()

    if found_clinical_record is not None:
        return jsonify({
            "msg": "este paciente ya tiene una ficha clínica creada"
        }), 400

    clinical_record.program = request.json.get("program")
    registration_date = request.json.get("registration_date")
    clinical_record.registration_date = date.fromisoformat(registration_date)
    clinical_record.barthel_index = request.json.get("barthel_index")
    clinical_record.zarit_scale_caregiver = request.json.get("zarit_scale_caregiver")
    clinical_record.patient_id = patient_id

    db.session.add(clinical_record)
    db.session.commit()

    return jsonify({
        "msg": "ficha creada correctamente"
    }), 200

@app.route("/add_drug", methods=["POST"])
def create_drug():
    drug = Drug()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    drug.name = request.json.get("name")
    drug.posology = request.json.get("posology")
    drug.clinical_record_id = clinical_record_id

    db.session.add(drug)
    db.session.commit()

    return jsonify({
        "msg": "medicamento añadido correctamente"
    }), 200

@app.route("/drugs", methods=["GET"])
def drugs():
    drug = Drug.query.all()
    drug_serialized = list(map( lambda drug: drug.serialize(), drug))
    return jsonify(drug_serialized)

@app.route("/create_control", methods=["POST"])
def create_control():
    control = Control()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    control.reason = request.json.get("reason")
    control.description = request.json.get("description")
    control.indications = request.json.get("indications")
    date_of_control = request.json.get("date_of_control")
    control.date_of_control = date.fromisoformat(date_of_control)
    control.clinical_record_id = clinical_record_id
    control.professional_id = request.json.get("professional_id")

    db.session.add(control)
    db.session.commit()

    return jsonify({
        "msg": "control añadido correctamente"
    }), 200

@app.route("/control", methods=["GET"])
def control():
    control = Control.query.all()
    control_serialized = list(map( lambda control: control.serialize(), control))
    return jsonify(control_serialized)


if __name__ == "__main__":
    app.run(host="localhost", port=8080)