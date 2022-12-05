from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.Integer, nullable=False, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    birth_date = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    alive = db.Column(db.Boolean, default=True)
    caregiver = db.relationship(
        "Caregiver", back_populates="patient", uselist=False)
    clinical_record = db.relationship(
        "Clinical_record", back_populates="patient", uselist=False)

    def __repr__(self):
        return "<Patient %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "rut": self.rut,
            "age": self.age,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "alive": self.alive
        }


class Caregiver(db.Model):
    __tablename__ = "caregivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    patient = db.relationship("Patient", back_populates="caregiver")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "rut": self.rut,
            "address": self.address,
            "patient_id": self.patient_id,
        }


class Clinical_record(db.Model):
    __tablename__ = "clinical_records"
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(100))
    registration_date = db.Column(db.Date)
    barthel_index = db.Column(db.String(100), nullable=False)
    zarit_scale_caregiver = db.Column(db.String(100))
    drugs = db.relationship("Drug")
    pathologies = db.relationship("Pathology")
    surgeries = db.relationship("Surgery")
    alergies = db.relationship("Alergy")
    habit = db.relationship(
        "Habit", back_populates="clinical_record", uselist=False)
    controls = db.relationship("Control", back_populates="clinical_record")
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    patient = db.relationship("Patient", back_populates="clinical_record")

    def serialize(self):
        return {
            "id": self.id,
            "program": self.program,
            "registration_date": self.registration_date,
            "barthel_index": self.barthel_index,
            "zarit_scale_caregiver": self.zarit_scale_caregiver,
            "patient_id": self.patient_id,
        }


class Drug(db.Model):
    __tablename__ = "drugs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posology = db.Column(db.String(100), nullable=False)
    clinical_record_id = db.Column(db.Integer, db.ForeignKey(
        "clinical_records.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "posology": self.posology,
            "clinical_record_id": self.clinical_record_id,
        }


class Pathology(db.Model):
    __tablename__ = "pathologies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey(
        "clinical_records.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clinical_record_id": self.clinical_record_id,
        }


class Surgery(db.Model):
    __tablename__ = "surgeries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey(
        "clinical_records.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clinical_record_id": self.clinical_record_id,
        }


class Alergy(db.Model):
    __tablename__ = "alergies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey(
        "clinical_records.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clinical_record_id": self.clinical_record_id,
        }


class Habit(db.Model):
    __tablename__ = "habits"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey(
        "clinical_records.id"), nullable=False)
    clinical_record = db.relationship(
        "Clinical_record", back_populates="habit")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clinical_record_id": self.clinical_record_id,
        }


class Control(db.Model):
    __tablename__ = "controls"
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    indications = db.Column(db.String(1000), nullable=False)
    date_of_control = db.Column(db.Date, nullable=False)
    professional = db.relationship("Professional")
    professional_id = db.Column(db.Integer, db.ForeignKey(
        "professionals.id"), nullable=False)
    clinical_record_id = db.Column(db.Integer, db.ForeignKey(
        "clinical_records.id"), nullable=False)
    clinical_record = db.relationship("Clinical_record")

    def serialize(self):
        return {
            "id": self.id,
            "reason": self.reason,
            "description": self.description,
            "indications": self.indications,
            "date_of_control": self.date_of_control,
            "professional_id": self.professional_id,
            "clinical_record_id": self.clinical_record_id,
        }


class Professional(db.Model):
    __tablename__ = "professionals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.Integer, nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Professional %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "rut": self.rut,
            "role": self.role,
            "email": self.email
        }
